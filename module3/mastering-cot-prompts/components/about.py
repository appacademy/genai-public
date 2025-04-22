import streamlit as st


def render_about():
    """Render the About/Help page."""
    st.header("About Chain-of-Thought Explorer")

    # Initialize needed components
    from utils.cot_builder import ChainOfThoughtBuilder

    builder = ChainOfThoughtBuilder()

    # Sidebar content
    with st.sidebar:
        st.divider()

        # Ollama status and model info
        st.markdown("## Settings")
        # Ollama status check
        ollama_client = builder.ollama_client
        ollama_status = (
            "✅ Connected" if ollama_client.check_health() else "❌ Not running"
        )
        st.write(f"Ollama API Status: {ollama_status}")

        # If Ollama is not running, show instructions
        if ollama_status == "❌ Not running":
            st.error("⚠️ Ollama is not running. Please start Ollama with Gemma 3 model.")
            st.info(
                "Run the following command in a terminal to start Ollama with Gemma 3:"
            )
            st.code("ollama run gemma3:4b")
            st.warning(
                "The app will continue to load, but LLM features won't work until Ollama is running."
            )

        # Model information
        st.caption("Using Ollama with Gemma 3 4B for CoT prompting.")
        st.write("**Model Info**: Gemma 3 4B")

        with st.expander("Model Details"):
            st.markdown(
                """
                **Gemma 3 4B Model:**
                - Running locally via Ollama
                - 128K token context window
                - No API key required
                - All processing happens on your machine
                - Fast response times
                """
            )

        with st.expander("ℹ️ Need Help?"):
            st.markdown(
                """
            This tool helps you understand and craft effective chain-of-thought prompts.
            
            **To get started:**
            1. Use the "Template Explorer" to understand different reasoning approaches
            2. Build your own prompts in the "CoT Prompt Builder" 
            3. Compare standard vs. CoT prompting in the "Comparison Tool"
            
            Navigate using the dropdown menu in the sidebar.
            """
            )

    st.markdown(
        """
    ## What is Chain-of-Thought Prompting?
    
    Chain-of-Thought (CoT) prompting is a technique that improves the reasoning capabilities of large language models by encouraging them to work through a problem step-by-step. Instead of asking for a direct answer, CoT prompting guides the model to break down complex problems into intermediate reasoning steps.
    
    ## Why is CoT Prompting Important?
    
    Research has shown that CoT prompting significantly improves performance on complex reasoning tasks like:
    - Mathematical problem-solving
    - Logical reasoning
    - Multi-step deduction
    - Code analysis
    - Policy application
    
    By making the reasoning process explicit, CoT prompting:
    - Reduces reasoning errors
    - Makes the model's thought process transparent and auditable
    - Improves consistency in answers
    - Handles more complex problems that require multiple steps
    
    ## Using This Tool
    
    This application allows you to:
    
    ### Explore Templates
    Browse different reasoning patterns and domain-specific templates to understand when to use each approach.
    
    ### Build CoT Prompts
    Craft effective chain-of-thought prompts by selecting domains and reasoning patterns, then test them with the Gemma 3 model via Ollama.
    
    ### Compare Approaches
    Run side-by-side comparisons of standard prompting versus chain-of-thought prompting to see the differences in responses.
    
    ### Customize Templates
    Create and save your own templates for reasoning patterns or domain-specific applications.
    
    ## Getting Started
    
    1. Begin by exploring the different reasoning templates to understand the structure of CoT prompts
    2. Try crafting a simple prompt in your domain of interest
    3. Run a comparison to see the difference between standard and CoT prompting
    4. Refine your approach based on the results
    
    ## Learn More
    
    For more information on Chain-of-Thought prompting, check out these resources:
    
    - [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) (Original research paper)
    - [Prompt Engineering Guide: Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
    - [Anthropic's Guide to Prompt Engineering](https://www.anthropic.com/index/prompting-guide)
    """
    )

    st.divider()

    st.markdown(
        """
    ## About This Application
    
    Chain-of-Thought Explorer was created as a learning tool to help students master prompt engineering techniques. The application demonstrates how to structure effective prompts that elicit clear, step-by-step reasoning from AI models.
    
    **Built with:**
    - Streamlit
    - Ollama with Gemma 3 4B
    - Python
    
    **Features:**
    - Interactive prompt building
    - Real-time API integration
    - Visualization of prompt effectiveness
    - Template customization and sharing
    """
    )
