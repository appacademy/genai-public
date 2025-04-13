import os
import streamlit as st
import matplotlib.pyplot as plt
import time
from datetime import datetime
from pathlib import Path
import requests

# Import our custom OllamaClient
from ollama_client import OllamaClient

# Configuration and setup
st.set_page_config(page_title="Text Completion Explorer", layout="wide")

# Initialize the Ollama client
client = OllamaClient(base_url="http://localhost:11434", model="gemma3:4b")

# Check if Ollama server is running
ollama_available = client.check_health()

# App title and description
st.title("Text Completion Explorer")
st.write(
    """
This tool demonstrates how Large Language Models generate text token by token. 
Watch the generation process in real-time and experiment with different temperature settings to understand 
how they affect output creativity and variability.
"""
)

# Display Ollama server status
if ollama_available:
    st.success("✅ Connected to Ollama server")
else:
    st.error(
        "❌ Cannot connect to Ollama server. Please make sure Ollama is running on http://localhost:11434"
    )

# Sidebar for settings
with st.sidebar:
    st.header("Settings")

    # Update model selection to use Ollama models
    model = st.selectbox("Select model:", ["gemma3:4b"])

    # Update client model when selection changes
    client.model = model

    max_tokens = st.slider(
        "Maximum length (tokens):", min_value=50, max_value=1000, value=250, step=50
    )

# Main content area
tab1, tab2 = st.tabs(["Single Generation", "Temperature Comparison"])

with tab1:
    st.header("Generate Text")

    # User input
    prompt = st.text_area(
        "Enter your prompt:",
        "Write a short story about a robot learning to paint.",
        height=100,
    )

    # Generation parameters
    col1, col2 = st.columns(2)

    with col1:
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher values mean more random completions. Lower values mean more deterministic completions.",
        )

    with col2:
        token_display_speed = st.slider(
            "Token display speed",
            min_value=0.0,
            max_value=0.1,
            value=0.02,
            step=0.01,
            help="Adjust how quickly tokens appear (in seconds). 0 for instant display.",
        )

    # Function to generate text with streaming and token highlighting
    def generate_text_streaming(
        prompt, temperature=0.7, model="gemma3:4b", max_tokens=500
    ):
        if not ollama_available:
            st.error(
                "Cannot connect to Ollama server. Please make sure Ollama is running."
            )
            return None

        try:
            # Create a container for the generated text
            result_container = st.empty()
            token_counter_container = st.empty()

            generated_text = ""
            tokens_generated = 0

            # Track the start time for calculating tokens per second
            start_time = time.time()

            # Update client model if different from current
            if client.model != model:
                client.model = model

            # TODO: Make the API call with streaming enabled
            # HINT: Use client.generate_stream with appropriate parameters
            # stream = client.generate_stream(...)

            # TODO: Process the stream of tokens
            # For each token in the stream:
            #   1. Check if token is an error message
            #   2. Get the new token
            #   3. Add it to the generated text
            #   4. Update the display with the latest token highlighted
            #   5. Calculate and display tokens per second
            #   6. Add optional delay based on token_display_speed

            # TODO: Display final statistics
            # Calculate and display the total tokens generated and generation speed

            return generated_text

        except Exception as e:
            st.error(f"Error generating text: {e}")
            return None

    # Generation button
    if st.button("Generate Text", key="generate_single"):
        with st.spinner("Generating..."):
            if not prompt:
                st.warning("Please enter a prompt first.")
            else:
                st.subheader("Generated Output:")
                generate_text_streaming(
                    prompt=prompt,
                    temperature=temperature,
                    model=model,
                    max_tokens=max_tokens,
                )

with tab2:
    st.header("Compare Temperature Settings")
    st.write(
        """
    This tab allows you to generate multiple completions for the same prompt with different temperature settings.
    Compare how temperature affects creativity, variability, and coherence.
    """
    )

    # User input
    compare_prompt = st.text_area(
        "Enter your prompt for comparison:",
        "Explain why the sky is blue in the style of a",
        height=80,
        key="compare_prompt",
    )

    # Add temperature options
    st.subheader("Temperature Settings to Compare")

    col1, col2, col3 = st.columns(3)

    with col1:
        compare_temp1 = st.slider("Temperature 1", 0.0, 2.0, 0.0, 0.1)
        compare_style1 = st.text_input(
            "Style description 1 (optional):", "scientific textbook"
        )

    with col2:
        compare_temp2 = st.slider("Temperature 2", 0.0, 2.0, 0.7, 0.1)
        compare_style2 = st.text_input(
            "Style description 2 (optional):", "children's story"
        )

    with col3:
        compare_temp3 = st.slider("Temperature 3", 0.0, 2.0, 1.4, 0.1)
        compare_style3 = st.text_input("Style description 3 (optional):", "poet")

    # Generate comparisons
    if st.button("Generate Comparisons"):
        if not ollama_available:
            st.error(
                "Cannot connect to Ollama server. Please make sure Ollama is running."
            )
        elif not compare_prompt:
            st.warning("Please enter a prompt first.")
        else:
            # Create columns for the comparisons
            comp_col1, comp_col2, comp_col3 = st.columns(3)

            # TODO: Implement comparison generation for each temperature setting
            # For each of the three columns:
            #   1. Display the temperature value as a header
            #   2. Combine the base prompt with the style description
            #   3. Call generate_text_streaming with appropriate parameters
            #   4. Display the results in the corresponding column

# Information section
with st.expander("How does temperature work in LLMs?"):
    st.write(
        """
    ## Understanding Temperature in LLMs
    
    **Temperature** is a hyperparameter that controls randomness in token selection during text generation.
    
    ### How it works:
    
    1. The LLM calculates probabilities for each potential next token based on the input and previous tokens
    2. These raw probabilities are modified by dividing logits (pre-softmax scores) by the temperature value
    3. The modified probabilities are then used to sample the next token
    
    ### Effects of different temperature values:
    
    - **Low temperature (0.0-0.3)**: 
        - More deterministic outputs
        - The model consistently selects the most probable tokens
        - Good for factual responses, code generation, or when consistency is important
        - Responses may be more generic and predictable
    
    - **Medium temperature (0.4-0.8)**:
        - Balanced between determinism and creativity
        - Some variation but still relatively coherent
        - Good for conversational responses and general content creation
    
    - **High temperature (0.9-2.0)**:
        - More random, creative outputs
        - The model more frequently selects lower-probability tokens
        - Good for brainstorming, creative writing, or generating diverse alternatives
        - May produce less coherent or factually accurate content
    
    ### Visual representation of token selection:
    """
    )

    # Create a visual example of token selection with different temperatures
    fig, ax = plt.subplots(1, 3, figsize=(15, 3))

    # Example token probabilities
    tokens = ["the", "a", "this", "one", "some"]
    probs_original = [0.6, 0.2, 0.1, 0.05, 0.05]

    # Function to apply temperature to probabilities (simplified)
    def apply_temp(probs, temp):
        import numpy as np

        # TODO: Implement temperature scaling for token probabilities
        # HINT: Follow these steps:
        #   1. Convert probabilities to logits using logarithm
        #   2. Apply temperature scaling to the logits
        #   3. Convert back to probabilities using exponential and normalization

        # Return the temperature-adjusted probabilities
        return probs  # Replace this with your implementation

    # Apply different temperatures
    probs_temp_0_2 = apply_temp(probs_original, 0.2)
    probs_temp_0_7 = apply_temp(probs_original, 0.7)
    probs_temp_1_5 = apply_temp(probs_original, 1.5)

    # Plot the probabilities
    ax[0].bar(tokens, probs_temp_0_2, color="skyblue")
    ax[0].set_title("Temperature = 0.2")
    ax[0].set_ylim(0, 1)

    ax[1].bar(tokens, probs_temp_0_7, color="skyblue")
    ax[1].set_title("Temperature = 0.7")
    ax[1].set_ylim(0, 1)

    ax[2].bar(tokens, probs_temp_1_5, color="skyblue")
    ax[2].set_title("Temperature = 1.5")
    ax[2].set_ylim(0, 1)

    for a in ax:
        a.set_ylabel("Probability")
        a.set_xlabel("Tokens")

    plt.tight_layout()
    st.pyplot(fig)

    st.write(
        """
    Notice how higher temperatures "flatten" the probability distribution, making it more likely 
    that the model will select less probable tokens. This is why high-temperature outputs are more 
    varied and sometimes surprising, while low-temperature outputs are more predictable.
    """
    )

# Advanced options expander
with st.expander("Advanced Options and Extensions"):
    st.write(
        """
    ## Extension Ideas for This Activity
    
    If you've completed the basic functionality, consider adding these features:
    
    1. **Token Probability Display**: 
       For APIs that provide token probabilities, visualize alternative tokens the model considered.
    
    2. **Context Window Visualization**: 
       Add a feature that shows how much of the context window is being used as generation proceeds.
    
    3. **Custom Stopping Criteria**: 
       Implement functionality to stop generation based on specific tokens or patterns.
    
    4. **Generation History Analysis**: 
       Build a system to analyze patterns across multiple saved generations.
    
    5. **Prompt Templates**: 
       Create a library of effective prompt templates that students can explore.
    """
    )

st.markdown("---")
st.caption("Created for LLM Introduction Module | Text Completion Explorer Activity")
