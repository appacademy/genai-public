import streamlit as st
from utils.cot_builder import ChainOfThoughtBuilder
from utils.cot_evaluator import CoTEvaluator
from utils.visualization import (
    format_prompt_for_display,
    create_step_breakdown_chart,
    highlight_text,
)


def render_prompt_builder():
    """Render the CoT Prompt Builder page."""
    st.header("Chain-of-Thought Prompt Builder")

    # Use the shared builder from session state
    builder = st.session_state.builder
    evaluator = CoTEvaluator()

    # Get session state for storing inputs and results
    if "problem_description" not in st.session_state:
        st.session_state.problem_description = ""
    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = ""
    if "api_response" not in st.session_state:
        st.session_state.api_response = ""
    if "evaluation_results" not in st.session_state:
        st.session_state.evaluation_results = None

    # Sidebar for domain and reasoning type selection
    with st.sidebar:
        st.subheader("Configuration")

        # Update session state when domain changes
        if "selected_domain" not in st.session_state:
            st.session_state.selected_domain = "code_analysis"

        def update_domain():
            st.session_state.selected_domain = domain

        domain = st.selectbox(
            "Select Domain",
            options=list(builder.domain_templates.keys()),
            help="The domain area for which to generate a prompt",
            on_change=update_domain,
            key="domain_selectbox",
        )

        reasoning_type = st.selectbox(
            "Select Reasoning Type",
            options=list(builder.reasoning_templates.keys()),
            help="The type of reasoning approach to use",
        )

        model = st.selectbox(
            "Select Model",
            options=["gemma3:4b", "gemma3:7b"],
            index=0,
            help="The Gemma 3 model to use (note: currently using 4B variant regardless of selection)",
            disabled=True,  # Currently only gemma3:4b is supported
        )

        st.caption("Currently only Gemma 3 4B is supported via Ollama")

        st.divider()

        # Show reasoning steps explanation
        st.subheader(f"{reasoning_type.replace('_', ' ').title()} Reasoning")
        st.markdown(builder.reasoning_templates[reasoning_type]["description"])

        # Show steps
        for i, step in enumerate(
            builder.reasoning_templates[reasoning_type]["structure"]
        ):
            st.markdown(f"**Step {i+1}:** {step}")

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

    # Create two columns for the main layout: left side (steps 1 and 2) and right side (step 3)
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("1. Enter Your Problem")

        # Get domain-specific placeholder and help text
        placeholder_text = "Enter your problem or question here..."
        help_text = "Describe the problem or question you want to analyze"

        if domain == "code_analysis":
            placeholder_text = "Enter a code snippet to be analyzed..."
            help_text = "Paste your code here for analysis of functionality, performance, and suggestions for improvement"
        elif domain == "hr_policy":
            placeholder_text = "Enter your HR-related question or situation..."
            help_text = "Describe an HR situation or policy question for analysis"
        elif domain == "custom":
            placeholder_text = "Enter your reasoning problem or question..."
            help_text = (
                "Describe any problem that benefits from structured, logical analysis"
            )

        # Problem description input with dynamic placeholder and help text
        problem_description = st.text_area(
            "Problem Description",
            value=st.session_state.problem_description,
            height=200,
            help=help_text,
            placeholder=placeholder_text,
        )

        # Update session state
        st.session_state.problem_description = problem_description

        # Generate prompt button
        if st.button("Generate Prompt", type="primary"):
            with st.spinner("Generating prompt..."):
                prompt = builder.build_cot_prompt(
                    problem_description=problem_description,
                    domain=domain,
                    reasoning_type=reasoning_type,
                )
                st.session_state.generated_prompt = prompt
                st.session_state.api_response = ""  # Clear previous response
                st.session_state.evaluation_results = None  # Clear previous evaluation

        # Section 2: Review Generated Prompt
        st.subheader("2. Review Generated Prompt")

        # Show prompt if available
        if st.session_state.generated_prompt:
            with st.expander("Prompt Preview", expanded=True):
                st.markdown(
                    format_prompt_for_display(st.session_state.generated_prompt)
                )

            # Copy button
            if st.button("Copy to Clipboard"):
                st.toast("Prompt copied to clipboard!")
                # Perform the replace operation outside the f-string
                escaped_prompt = st.session_state.generated_prompt.replace('`', '\\`')
                # Use the escaped prompt in the JavaScript snippet
                st.markdown(
                    f"""
                    <script>
                        const text = `{escaped_prompt}`;
                        navigator.clipboard.writeText(text);
                    </script>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Generate a prompt to see it here.")

    with right_col:
        # Section 3: Generate and Analyze Response
        st.subheader("3. Generate and Analyze Response")

        # Advanced options in an expander
        with st.expander("Advanced Options"):
            st.subheader("Customize Template")

            # Allow customization of context
            custom_context = st.text_area(
                "Custom Context",
                value=builder.domain_templates[domain]["context"],
                help="Customize the context section of the prompt",
            )

            # Allow customization of constraints
            custom_constraints = st.text_area(
                "Custom Constraints",
                value="\n".join(builder.domain_templates[domain]["constraints"]),
                help="Customize the constraints section (one per line)",
            )

            # Apply customizations button
            if st.button("Apply Customizations"):
                # Parse constraints from text area (one per line)
                constraints_list = [
                    c.strip() for c in custom_constraints.split("\n") if c.strip()
                ]

                # Create custom sections
                custom_sections = {
                    "context": custom_context,
                    "constraints": constraints_list,
                }

                # Regenerate prompt with customizations
                prompt = builder.build_cot_prompt(
                    problem_description=problem_description,
                    domain=domain,
                    reasoning_type=reasoning_type,
                    custom_sections=custom_sections,
                )
                st.session_state.generated_prompt = prompt
                st.success("Customizations applied to prompt!")

        # Execute prompt button
        if st.session_state.generated_prompt and st.button("Execute Prompt"):
            with st.spinner("Executing prompt with Gemma 3 via Ollama..."):
                response = builder.execute_prompt(
                    prompt=st.session_state.generated_prompt, model=model
                )
                st.session_state.api_response = response

                # Evaluate the response
                evaluation = evaluator.evaluate_response(
                    problem=problem_description, response=response, domain=domain
                )
                st.session_state.evaluation_results = evaluation

        # Display response and evaluation if available
        if st.session_state.api_response:
            # Display response and evaluation side by side without nesting columns
            st.subheader("Response")
            # Highlight reasoning indicators in the response
            highlighted_response = evaluator.highlight_reasoning_steps(
                st.session_state.api_response
            )
            st.markdown(highlighted_response)

            st.subheader("Evaluation")
            if st.session_state.evaluation_results:
                eval_results = st.session_state.evaluation_results

                # Create metrics display without nested columns
                st.write(
                    "**Overall Score:** " + f"{eval_results['overall_score']:.1f}/10"
                )
                st.write(
                    "**Domain Relevance:** "
                    + f"{eval_results['domain_relevance_score']:.1f}/10"
                )
                st.write(
                    "**Completeness:** "
                    + f"{eval_results['completeness_score']:.1f}/10"
                )

                st.divider()

                # Create breakdown chart
                create_step_breakdown_chart(
                    eval_results["reasoning_steps"],
                    eval_results["word_count"],
                    eval_results["domain_keyword_matches"],
                )

                # Save results button
                if st.button("Save Results"):
                    save_result = builder.save_results(
                        {
                            "prompt": st.session_state.generated_prompt,
                            "response": st.session_state.api_response,
                            "evaluation": eval_results,
                        }
                    )
                    st.success(save_result)
