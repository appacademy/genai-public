import streamlit as st
import os
import json
from dotenv import load_dotenv
from utils.ollama_client import OllamaClient
from utils.cot_builder import ChainOfThoughtBuilder

# Import components
from components.prompt_builder import render_prompt_builder
from components.comparison_tool import render_comparison_tool
from components.template_explorer import render_template_explorer
from components.about import render_about

# Load environment variables (kept for other possible env vars)
load_dotenv()

# Initialize a shared ChainOfThoughtBuilder in session state for persistence
if "builder" not in st.session_state:
    st.session_state.builder = ChainOfThoughtBuilder()

# Initialize Ollama client
ollama_client = OllamaClient()

# Set page configuration
st.set_page_config(
    page_title="Chain-of-Thought Explorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Include external CSS
with open("static/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main title at the top of the page
st.title("🧠 Chain-of-Thought Explorer")
st.caption("Mastering Step-by-Step Reasoning in LLM Prompts")

# Define sidebar content - just navigation
with st.sidebar:
    # Navigation at the top of the sidebar
    st.title("Navigation")
    page = st.selectbox(
        "Select a tool",
        options=[
            "CoT Prompt Builder",
            "Comparison Tool",
            "Template Explorer",
            "About/Help",
        ],
        index=0,
    )

# Render the appropriate component based on navigation selection
if page == "CoT Prompt Builder":
    render_prompt_builder()
elif page == "Comparison Tool":
    render_comparison_tool()
elif page == "Template Explorer":
    render_template_explorer()
else:  # About/Help
    render_about()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888;">
    Chain-of-Thought Explorer | Created for educational purposes | Version 1.1
    </div>
    """,
    unsafe_allow_html=True,
)
