import matplotlib.pyplot as plt
import io
import base64
import streamlit as st
import re
from typing import Dict, List, Tuple


def highlight_text(text: str, indicators: List[str]) -> str:
    """Highlight specified words in text for Streamlit markdown display."""
    for indicator in indicators:
        # Match whole words with word boundaries
        pattern = re.compile(rf"\b{re.escape(indicator)}\b", re.IGNORECASE)
        text = pattern.sub(f"**{indicator}**", text)
    return text


def create_comparison_chart(std_metrics: Dict, cot_metrics: Dict) -> None:
    """Create a bar chart comparing standard and CoT metrics."""
    # Prepare data for plotting
    metrics = {
        "Word Count": (
            std_metrics["standard_word_count"],
            cot_metrics["cot_word_count"],
        ),
        "Reasoning Indicators": (
            std_metrics["standard_reasoning_indicators"],
            cot_metrics["cot_reasoning_indicators"],
        ),
    }

    # Create a DataFrame for plotting
    labels = list(metrics.keys())
    standard_values = [metrics[label][0] for label in labels]
    cot_values = [metrics[label][1] for label in labels]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set up bar positions
    x = range(len(labels))
    width = 0.35

    # Create grouped bar chart
    rects1 = ax.bar(
        [pos - width / 2 for pos in x],
        standard_values,
        width,
        label="Standard",
        color="#3498db",
    )
    rects2 = ax.bar(
        [pos + width / 2 for pos in x],
        cot_values,
        width,
        label="Chain-of-Thought",
        color="#e74c3c",
    )

    # Add labels and title
    ax.set_ylabel("Count")
    ax.set_title("Standard vs Chain-of-Thought Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Add value labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)


def create_radar_chart(metrics: Dict) -> None:
    """Create a radar chart for evaluation metrics."""
    # Metrics to plot
    categories = ["Domain Relevance", "Completeness", "Overall Score"]
    values = [
        metrics["domain_relevance_score"],
        metrics["completeness_score"],
        metrics["overall_score"],
    ]

    # Convert to radar format with closed loop
    categories = categories + [categories[0]]
    values = values + [values[0]]

    # Calculate angles for radar chart
    angles = [
        n / float(len(categories) - 1) * 2 * 3.14159 for n in range(len(categories))
    ]

    # Create figure and polar axis
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plot the radar chart
    ax.plot(angles, values, linewidth=2, linestyle="solid", color="#3498db")
    ax.fill(angles, values, alpha=0.25, color="#3498db")

    # Set the angle labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories[:-1])

    # Set y-axis limits and labels
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"])

    # Add title
    plt.title("Evaluation Metrics Radar Chart", size=15, y=1.1)

    # Display in Streamlit
    st.pyplot(fig)


def create_step_breakdown_chart(
    steps: int, word_count: int, keyword_count: int
) -> None:
    """Create a horizontal bar chart for reasoning steps breakdown."""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Prepare data
    metrics = {
        "Reasoning Steps": steps,
        "Keywords Matched": keyword_count,
        "Words per Step": word_count / max(1, steps),
    }

    # Create horizontal bar chart
    bars = ax.barh(
        list(metrics.keys()),
        list(metrics.values()),
        color=["#3498db", "#2ecc71", "#f39c12"],
    )

    # Add values to end of bars
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.1f}",
            ha="left",
            va="center",
        )

    # Set labels and title
    ax.set_xlabel("Count")
    ax.set_title("Response Breakdown")

    # Add a grid
    ax.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)


def get_color_scale(score: float) -> str:
    """Get a color from red to green based on score (0-10)."""
    # Normalize score to 0-1
    normalized = max(0, min(score, 10)) / 10

    # Create RGB values for gradient from red to yellow to green
    if normalized < 0.5:
        # Red to yellow
        r = 1.0
        g = normalized * 2
        b = 0.0
    else:
        # Yellow to green
        r = (1.0 - normalized) * 2
        g = 1.0
        b = 0.0

    # Convert to hex
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def format_prompt_for_display(prompt: str) -> str:
    """Format a prompt for better display in Streamlit."""
    # Replace markdown headings with styled headings
    prompt = re.sub(r"^# (.+)$", r"### \1", prompt, flags=re.MULTILINE)

    # Check if prompt contains "code_analysis" domain indicator
    is_code_domain = (
        "You are a senior software developer" in prompt or "code_analysis" in prompt
    )

    # Check if there are already code blocks with backticks
    has_code_blocks = re.search(r"```(.+?)```", prompt, flags=re.DOTALL) is not None

    # Only apply code detection for code-related prompts
    if is_code_domain and not has_code_blocks:
        # Common code patterns (indented blocks, function definitions, if statements, etc.)
        code_patterns = [
            # One-line function definition pattern (matches the example problem case)
            r"(def\s+\w+\s*\([^)]*\)\s*:.+?(?:if|for|while|return|[{}).;]).*?(?:return\s+.+?)?)",
            # Function definition pattern
            r"(def\s+\w+\s*\([^)]*\)\s*:.*?(?:\n\s+.+?)+)",
            # Class definition pattern
            r"(class\s+\w+(?:\([^)]*\))?\s*:.*?(?:\n\s+.+?)+)",
            # Common programming constructs
            r"((import|from)\s+[a-zA-Z0-9_.]+(?: import [a-zA-Z0-9_., ]+)?)",
            # Blocks with brackets or braces that look like code
            r"(\{\s*\n(?:\s+[a-zA-Z0-9_]+: .+\n)+\s*\})",
        ]

        for pattern in code_patterns:

            def wrap_with_code_block(match):
                code = match.group(1)
                # Format code for better readability if it's a one-liner
                if "\n" not in code and "def " in code and ":" in code:
                    # Try to format the code by adding newlines and indentation
                    try:
                        formatted_code = code.replace(": ", ":\n    ")
                        formatted_code = re.sub(
                            r"(\s*)(if|for|while)(\s+)", r"\n    \1\2\3", formatted_code
                        )
                        formatted_code = re.sub(
                            r"(return\s+)", r"\n    \1", formatted_code
                        )
                        code = formatted_code
                    except:
                        # If any error in formatting, use the original code
                        pass

                # Ensure there's a line break before the code block
                if not code.startswith("\n"):
                    code = "\n" + code

                return f"\n```python{code}\n```"

            prompt = re.sub(pattern, wrap_with_code_block, prompt, flags=re.DOTALL)

    # Ensure existing code blocks have proper syntax highlighting
    prompt = re.sub(
        r"```(?!python)(?!\n```)(.*?)```", r"```python\1```", prompt, flags=re.DOTALL
    )

    # Fix code blocks that might have been nested
    prompt = re.sub(
        r"```python\n```python(.*?)```\n```", r"```python\1```", prompt, flags=re.DOTALL
    )

    # Fix incorrect closing tags (ensure they're just ```, not ```python)
    prompt = re.sub(r"```python$", r"```", prompt, flags=re.MULTILINE)
    prompt = re.sub(r"```python\s*$", r"```", prompt, flags=re.MULTILINE)

    return prompt


def create_word_count_indicators_chart(word_count: int, indicators: int) -> None:
    """Create a simple chart showing word count and reasoning indicators."""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))

    # Prepare data
    metrics = {"Word Count": word_count, "Reasoning Indicators": indicators}

    # Normalize word count for better visualization
    metrics["Word Count"] = metrics["Word Count"] / 100

    # Create bar chart
    bars = ax.bar(
        list(metrics.keys()), list(metrics.values()), color=["#3498db", "#e74c3c"]
    )

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        value_text = f"{height}"
        if bar.get_x() < 1:  # Word count bar
            value_text = f"{height * 100} words"
        ax.annotate(
            value_text,
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    # Set labels and title
    ax.set_ylabel("Count")
    ax.set_title("Response Metrics")

    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)
