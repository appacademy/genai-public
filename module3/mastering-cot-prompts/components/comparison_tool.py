import streamlit as st
from utils.cot_builder import ChainOfThoughtBuilder
from utils.visualization import create_comparison_chart, highlight_text


def render_comparison_tool():
    """Render the Comparison Tool page."""
    st.header("Standard vs. Chain-of-Thought Comparison")

    # Use the shared builder from session state
    builder = st.session_state.builder

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

    # Initialize session state for storing inputs and results
    if "comparison_problem" not in st.session_state:
        st.session_state.comparison_problem = ""
    if "comparison_results" not in st.session_state:
        st.session_state.comparison_results = None

    # Main input section
    st.subheader("Enter Problem for Comparison")

    # Problem description
    problem_description = st.text_area(
        "Problem Description",
        value=st.session_state.comparison_problem,
        height=150,
        help="Describe the problem or question you want to analyze with both approaches",
        placeholder="Enter your problem or question here...",
    )

    # Update session state
    st.session_state.comparison_problem = problem_description

    # Domain selection
    domain = st.selectbox(
        "Select Domain",
        options=list(builder.domain_templates.keys()),
        help="The domain area for the comparison",
    )

    # Model selection
    model = st.selectbox(
        "Select Model",
        options=["gemma3:4b"],
        index=0,
        help="The model to use for the comparison (currently only Gemma 3 4B is supported)",
        disabled=True,  # Currently only Gemma 3 4B is supported
    )

    st.caption("Currently only Gemma 3 4B is supported via Ollama")

    # Run comparison button
    if problem_description and st.button("Run Comparison", type="primary"):
        with st.spinner(
            "Running comparison with Gemma 3 via Ollama... This may take a moment."
        ):
            comparison_results = builder.compare_with_standard_prompt(
                problem_description=problem_description, domain=domain, model=model
            )
            st.session_state.comparison_results = comparison_results

    # Display results if available
    if st.session_state.comparison_results:
        results = st.session_state.comparison_results

        # Display analysis summary
        st.subheader("Analysis Summary")
        st.markdown(results["analysis"])

        # Create visualization of metrics
        st.subheader("Metrics Comparison")

        # Display metrics with visualization
        create_comparison_chart(results["metrics"], results["metrics"])

        # Tabs for prompts and responses
        tab1, tab2 = st.tabs(["Prompts", "Responses"])

        with tab1:
            # Side-by-side prompt comparison
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Standard Prompt")
                st.code(results["standard_prompt"], language="markdown")

            with col2:
                st.subheader("Chain-of-Thought Prompt")
                st.code(results["cot_prompt"], language="markdown")

        with tab2:
            # Side-by-side response comparison
            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Standard Response")
                st.markdown(results["highlighted_standard_response"])
                st.text(f"Word count: {results['metrics']['standard_word_count']}")
                st.text(
                    f"Reasoning indicators: {results['metrics']['standard_reasoning_indicators']}"
                )

            with col4:
                st.subheader("Chain-of-Thought Response")
                st.markdown(results["highlighted_cot_response"])
                st.text(f"Word count: {results['metrics']['cot_word_count']}")
                st.text(
                    f"Reasoning indicators: {results['metrics']['cot_reasoning_indicators']}"
                )

        # Save results button
        if st.button("Save Comparison Results"):
            save_result = builder.save_results(results)
            st.success(save_result)

        # Analysis insights
        with st.expander("Comparison Insights"):
            st.subheader("What to Look For")
            st.markdown(
                """
            When comparing standard vs. Chain-of-Thought prompting, pay attention to:
            
            1. **Structure and Organization**: CoT responses typically show a clearer step-by-step structure
            2. **Reasoning Indicators**: Words like "first," "because," "therefore" indicate explicit reasoning
            3. **Depth of Analysis**: CoT often explores the problem more thoroughly
            4. **Alternative Perspectives**: CoT may consider multiple viewpoints or approaches
            5. **Conclusion Quality**: Does the conclusion follow logically from the reasoning?
            
            Chain-of-Thought prompting generally shows the most improvement for complex reasoning tasks that benefit from breaking down the problem into explicit steps.
            """
            )
