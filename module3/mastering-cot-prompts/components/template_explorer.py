import streamlit as st
from utils.cot_builder import ChainOfThoughtBuilder
import json


def render_template_explorer():
    """Render the Template Explorer page."""
    st.header("Chain-of-Thought Template Explorer")

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

    # Create tabs for different exploration views
    tab1, tab2, tab3 = st.tabs(
        ["Reasoning Templates", "Domain Templates", "Customization"]
    )

    with tab1:
        st.subheader("Reasoning Approaches")
        st.markdown(
            """
        Chain-of-Thought reasoning involves breaking down complex problems into 
        sequential steps. Different reasoning approaches are suited for different 
        types of problems. Explore the templates below to understand when to use each approach.
        """
        )

        # Display reasoning templates in three columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Sequential Reasoning")
            st.markdown(builder.reasoning_templates["sequential"]["description"])
            st.markdown(
                "**When to use:** Problems requiring step-by-step analysis with clear progression."
            )
            st.markdown("##### Structure:")
            for i, step in enumerate(
                builder.reasoning_templates["sequential"]["structure"]
            ):
                st.markdown(f"{i+1}. {step}")

            # Example problem for sequential reasoning
            with st.expander("Example Application"):
                st.markdown(
                    """
                **Problem:** Debug a function that should calculate factorial but returns incorrect results.
                
                **Approach:**
                1. **Understand the problem:** Identify what factorial is and what the function should do.
                2. **Break down the problem:** Analyze the code line by line.
                3. **Address each part:** Identify the bug in the calculation.
                4. **Integrate solution:** Fix the code with the correct factorial logic.
                """
                )

        with col2:
            st.subheader("Criteria-based Evaluation")
            st.markdown(builder.reasoning_templates["criteria_based"]["description"])
            st.markdown(
                "**When to use:** Decision-making problems with multiple factors to consider."
            )
            st.markdown("##### Structure:")
            for i, step in enumerate(
                builder.reasoning_templates["criteria_based"]["structure"]
            ):
                st.markdown(f"{i+1}. {step}")

            # Example problem for criteria-based reasoning
            with st.expander("Example Application"):
                st.markdown(
                    """
                **Problem:** Decide which database technology to use for a new project.
                
                **Approach:**
                1. **Identify criteria:** Scalability, query complexity, cost, maintenance, community support.
                2. **Assess each option:** Evaluate MongoDB, PostgreSQL, and MySQL against each criterion.
                3. **Weigh importance:** Determine which criteria matter most for this specific project.
                4. **Form conclusion:** Select the database that best matches the weighted criteria.
                """
                )

        with col3:
            st.subheader("Comparative Analysis")
            st.markdown(builder.reasoning_templates["comparative"]["description"])
            st.markdown(
                "**When to use:** Problems requiring comparison between multiple options or approaches."
            )
            st.markdown("##### Structure:")
            for i, step in enumerate(
                builder.reasoning_templates["comparative"]["structure"]
            ):
                st.markdown(f"{i+1}. {step}")

            # Example problem for comparative reasoning
            with st.expander("Example Application"):
                st.markdown(
                    """
                **Problem:** Compare React vs. Angular for a new web application.
                
                **Approach:**
                1. **Identify options:** React and Angular as frontend frameworks.
                2. **List pros of each:** React's flexibility, Angular's built-in features.
                3. **List cons of each:** React's minimal approach, Angular's learning curve.
                4. **Compare directly:** Contrast performance, ecosystem, and team expertise.
                5. **Recommend with justification:** Select one with clear reasoning.
                """
                )

    with tab2:
        st.subheader("Domain-Specific Templates")
        st.markdown(
            """
        Chain-of-Thought prompts can be tailored for specific domains. Each domain has unique 
        requirements, terminology, and evaluation criteria. Explore how CoT prompting changes 
        across different domains.
        """
        )

        # Domain selection dropdown
        domain = st.selectbox(
            "Select Domain to Explore", options=list(builder.domain_templates.keys())
        )

        # Display domain template details
        domain_info = builder.domain_templates[domain]

        st.markdown(f"### {domain.replace('_', ' ').title()} Domain")

        # Display context
        st.markdown("#### Context")
        st.markdown(domain_info["context"])

        # Display instruction template
        st.markdown("#### Instruction Template")
        st.code(domain_info["instruction_template"])

        # Display constraints
        st.markdown("#### Domain-Specific Constraints")
        for constraint in domain_info["constraints"]:
            st.markdown(f"- {constraint}")

        # Display examples if available
        if domain_info["example"] and "problem" in domain_info["example"]:
            with st.expander("Domain Example", expanded=True):
                st.markdown("#### Example Problem")
                st.code(domain_info["example"]["problem"])

                st.markdown("#### Example Solution")
                st.markdown(domain_info["example"]["reasoning"])

    with tab3:
        st.subheader("Customize Your Templates")
        st.markdown(
            """
        Chain-of-Thought templates can be customized to fit your specific needs.
        Create new templates or modify existing ones to improve results for your
        specific use cases.
        """
        )

        # Template type selection
        template_type = st.radio(
            "Select Template Type to Customize",
            options=["Reasoning Template", "Domain Template"],
        )

        if template_type == "Reasoning Template":
            # Reasoning template customization
            template_name = st.text_input("Template Name", value="custom_reasoning")
            description = st.text_area("Description", value="Custom reasoning approach")

            # Structure steps
            st.markdown("#### Structure Steps")
            steps = []
            for i in range(1, 6):  # Allow up to 5 steps
                step = st.text_input(f"Step {i}", key=f"step_{i}")
                if step:
                    steps.append(step)

            if st.button("Save Custom Reasoning Template"):
                if not template_name or not description or not steps:
                    st.error("Please fill out all fields")
                else:
                    builder.add_template(
                        "reasoning",
                        template_name,
                        {"description": description, "structure": steps},
                    )
                    st.success(
                        f"Template '{template_name}' saved! You can now use it in the Prompt Builder."
                    )

        else:
            # Domain template customization
            template_name = st.text_input("Template Name", value="custom_domain")
            context = st.text_area(
                "Context", value="You are an expert analyzing a specific problem."
            )
            instruction_template = st.text_area(
                "Instruction Template", value="{problem}"
            )

            # Constraints
            st.markdown("#### Domain Constraints")
            constraints = []
            for i in range(1, 6):  # Allow up to 5 constraints
                constraint = st.text_input(f"Constraint {i}", key=f"constraint_{i}")
                if constraint:
                    constraints.append(constraint)

            if st.button("Save Custom Domain Template"):
                if not template_name or not context or not instruction_template:
                    st.error("Please fill out all required fields")
                else:
                    builder.add_template(
                        "domain",
                        template_name,
                        {
                            "context": context,
                            "instruction_template": instruction_template,
                            "constraints": constraints,
                            "example": {},
                        },
                    )
                    st.success(
                        f"Template '{template_name}' saved! You can now use it in the Prompt Builder."
                    )

        # Export/Import section
        st.divider()
        st.subheader("Export/Import Templates")

        # Export templates
        if st.button("Export Templates"):
            templates = {
                "reasoning_templates": builder.reasoning_templates,
                "domain_templates": builder.domain_templates,
            }
            json_str = json.dumps(templates, indent=2)
            st.download_button(
                label="Download Templates JSON",
                data=json_str,
                file_name="cot_templates.json",
                mime="application/json",
            )

        # Import templates
        uploaded_file = st.file_uploader("Import Templates", type="json")
        if uploaded_file is not None:
            try:
                imported_templates = json.load(uploaded_file)
                if (
                    "reasoning_templates" in imported_templates
                    and "domain_templates" in imported_templates
                ):
                    for name, template in imported_templates[
                        "reasoning_templates"
                    ].items():
                        builder.add_template("reasoning", name, template)

                    for name, template in imported_templates[
                        "domain_templates"
                    ].items():
                        builder.add_template("domain", name, template)

                    st.success("Templates imported successfully!")
                else:
                    st.error("Invalid template file format")
            except Exception as e:
                st.error(f"Error importing templates: {str(e)}")
