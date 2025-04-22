import pandas as pd
from datetime import datetime
from typing import Dict, List
import re
import matplotlib.pyplot as plt
import io
import base64


class CoTEvaluator:
    """Evaluates the quality of chain-of-thought responses."""

    def __init__(self):
        self.evaluation_log = []

    def evaluate_response(self, problem: str, response: str, domain: str) -> Dict:
        """
        Evaluate a CoT response based on completeness, reasoning quality, and domain relevance.

        Returns a dictionary with evaluation metrics.
        """
        # Count reasoning steps
        steps = len(
            [
                line
                for line in response.split("\n")
                if line.strip().startswith(
                    (
                        "1.",
                        "2.",
                        "3.",
                        "4.",
                        "5.",
                        "6.",
                        "7.",
                        "8.",
                        "9.",
                        "10.",
                        "First",
                        "Second",
                        "Third",
                        "Fourth",
                        "Fifth",
                        "Next",
                        "Finally",
                        "Lastly",
                    )
                )
            ]
        )

        # Basic metrics
        word_count = len(response.split())
        sentences = response.split(".")
        avg_sentence_length = word_count / max(1, len(sentences))

        # Domain-specific keyword check
        domain_keywords = {
            "code_analysis": [
                "code",
                "function",
                "performance",
                "efficiency",
                "algorithm",
                "bug",
                "error",
                "improvement",
                "refactor",
                "complexity",
            ],
            "hr_policy": [
                "policy",
                "employee",
                "compliance",
                "regulation",
                "fair",
                "consistent",
                "legal",
                "requirement",
                "balance",
                "workplace",
            ],
            "custom": [
                "analysis",
                "evaluation",
                "assessment",
                "consider",
                "examine",
                "factor",
                "impact",
                "recommendation",
                "solution",
                "approach",
            ],
        }

        keywords = domain_keywords.get(domain, [])
        keyword_count = sum(
            1 for keyword in keywords if keyword.lower() in response.lower()
        )

        result = {
            "reasoning_steps": steps,
            "word_count": word_count,
            "avg_sentence_length": avg_sentence_length,
            "domain_keyword_matches": keyword_count,
            "domain_relevance_score": min(10, keyword_count * 2),
            "completeness_score": min(10, steps * 2),
        }

        # Calculate overall quality score (simple weighted average)
        result["overall_score"] = (
            result["domain_relevance_score"] * 0.4 + result["completeness_score"] * 0.6
        )

        # Log the evaluation
        self.evaluation_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "problem": problem,
                "domain": domain,
                "metrics": result,
            }
        )

        return result

    def get_evaluation_summary(self) -> pd.DataFrame:
        """Get a summary of all evaluations as a pandas DataFrame."""
        if not self.evaluation_log:
            return pd.DataFrame()

        return pd.DataFrame(
            [
                {
                    "timestamp": entry["timestamp"],
                    "domain": entry["domain"],
                    "reasoning_steps": entry["metrics"]["reasoning_steps"],
                    "word_count": entry["metrics"]["word_count"],
                    "domain_relevance": entry["metrics"]["domain_relevance_score"],
                    "completeness": entry["metrics"]["completeness_score"],
                    "overall_score": entry["metrics"]["overall_score"],
                }
                for entry in self.evaluation_log
            ]
        )

    def highlight_reasoning_steps(self, response: str) -> str:
        """Highlight reasoning steps in a response for better visualization."""
        # Pattern for numbered steps
        numbered_pattern = (
            r"(^|\n)(\d+\.|\b(First|Second|Third|Fourth|Fifth|Next|Finally|Lastly)\b)"
        )

        # Replace with markdown emphasis
        highlighted = re.sub(numbered_pattern, r"\1**\2**", response)

        # Return the highlighted text
        return highlighted

    def plot_metrics(self, metrics: Dict) -> str:
        """Generate a plot of evaluation metrics and return as base64 encoded string."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Prepare data
        metrics_to_plot = {
            "Domain Relevance": metrics["domain_relevance_score"],
            "Completeness": metrics["completeness_score"],
            "Overall Score": metrics["overall_score"],
        }

        # Create horizontal bar chart
        bars = ax.barh(
            list(metrics_to_plot.keys()),
            list(metrics_to_plot.values()),
            color=["#3498db", "#2ecc71", "#f39c12"],
        )

        # Add values to end of bars
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}",
                ha="left",
                va="center",
            )

        # Set limits and labels
        ax.set_xlim(0, 10)
        ax.set_xlabel("Score (0-10)")
        ax.set_title("Evaluation Metrics")

        # Add a grid
        ax.grid(True, linestyle="--", alpha=0.7)

        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Convert to base64 string
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)

        return img_str

    def compare_metrics(self, standard_metrics: Dict, cot_metrics: Dict) -> str:
        """Generate a comparison plot of standard vs CoT metrics and return as base64 encoded string."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Prepare data
        metrics = ["Word Count", "Reasoning Indicators"]
        standard_values = [
            standard_metrics["standard_word_count"],
            standard_metrics["standard_reasoning_indicators"],
        ]
        cot_values = [
            cot_metrics["cot_word_count"],
            cot_metrics["cot_reasoning_indicators"],
        ]

        # Normalize word count for better visualization
        max_word_count = max(standard_values[0], cot_values[0])
        standard_values[0] = (standard_values[0] / max_word_count) * 10
        cot_values[0] = (cot_values[0] / max_word_count) * 10

        # Set up positions
        x = range(len(metrics))
        width = 0.35

        # Create grouped bar chart
        rects1 = ax.bar(
            [i - width / 2 for i in x],
            standard_values,
            width,
            label="Standard",
            color="#3498db",
        )
        rects2 = ax.bar(
            [i + width / 2 for i in x],
            cot_values,
            width,
            label="Chain-of-Thought",
            color="#e74c3c",
        )

        # Add labels and title
        ax.set_ylabel("Score")
        ax.set_title("Standard vs Chain-of-Thought Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()

        # Add value labels
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(
                    f"{height:.1f}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )

        autolabel(rects1)
        autolabel(rects2)

        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Convert to base64 string
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)

        return img_str
