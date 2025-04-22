import streamlit as st
from models.prompt_template import PromptTemplate


def show_create_prompt():
    """Display the create prompt page."""

    # Initialize session state variables for template loading and form clearing
    if "load_template" not in st.session_state:
        st.session_state.load_template = None

    if "clear_form" not in st.session_state:
        st.session_state.clear_form = False

    # Handle form clearing if requested
    if st.session_state.clear_form:
        # Initialize form fields with empty values
        st.session_state.context = ""
        st.session_state.instruction = ""
        st.session_state.response_format = ""
        st.session_state.constraints = ""
        st.session_state.examples = [{"query": "", "response": ""}]
        # We don't reset template_name here to avoid the error

        # Reset the clear_form flag
        st.session_state.clear_form = False

    # Process template loading if requested
    if st.session_state.load_template:
        sample_templates = {
            "SQL Optimizer": {
                "context": "You are an expert SQL developer helping to optimize database queries.",
                "instruction": "Review the following SQL query and suggest optimizations to improve its performance.",
                "response_format": "Provide your suggestions in a numbered list, with each item explaining: 1) The issue identified, 2) Why it's a problem, 3) The recommended solution.",
                "constraints": "Focus only on performance optimizations, not on syntax or style improvements. Limit your response to the top 3-5 most impactful changes.",
                "examples": [
                    {
                        "query": "SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id WHERE orders.date > '2023-01-01'",
                        "response": "1. Issue: Using SELECT *\n   Problem: Retrieving all columns increases I/O and network transfer.\n   Solution: Select only needed columns explicitly.\n\n2. Issue: Missing index on orders.date\n   Problem: The WHERE clause filters on a non-indexed column.\n   Solution: Add an index on orders.date for this common query pattern.",
                    }
                ],
            },
            "Summarizer": {
                "context": "You are a professional content summarizer.",
                "instruction": "Summarize the following text while preserving the key information and main points.",
                "response_format": "Provide a concise summary in 2-3 paragraphs.",
                "constraints": "Maintain factual accuracy. Do not introduce information not present in the original text. Use simple, clear language.",
                "examples": [
                    {
                        "query": 'Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.',
                        "response": "Artificial Intelligence (AI) refers to machines exhibiting intelligence, contrasting with the natural intelligence of humans and animals. The field focuses on studying intelligent agents—systems that perceive their surroundings and act to achieve goals effectively.\n\nWhile AI was once defined as machines mimicking human cognitive abilities like learning and problem-solving, modern AI researchers have shifted away from this anthropocentric definition. Instead, they conceptualize AI in terms of rationality and rational actions, which broadens the understanding of how intelligence can manifest beyond human-like characteristics.",
                    }
                ],
            },
        }

        template_data = sample_templates[st.session_state.load_template]

        # Store the template name before resetting for success message
        template_name_loaded = st.session_state.load_template

        # Initialize form fields with template data
        st.session_state.context = template_data["context"]
        st.session_state.instruction = template_data["instruction"]
        st.session_state.response_format = template_data["response_format"]
        st.session_state.constraints = template_data["constraints"]
        st.session_state.examples = template_data["examples"]
        st.session_state.template_name = template_name_loaded

        # Reset load_template so it doesn't reload on next rerun
        st.session_state.load_template = None

        # Show success message
        st.success(f"Loaded sample template: {template_name_loaded}")

    st.header("Create Prompt Template")

    # Educational sidebar
    with st.expander("About the Five-Part Prompt Structure", expanded=False):
        st.info(
            """
        **Context**: Provides background information and sets the role for the AI.
        
        **Instruction**: The main task or request - this is the only required component.
        
        **Response Format**: How you want the response structured (e.g., bullet points, JSON).
        
        **Constraints**: Limitations or requirements for the response.
        
        **Examples**: Sample inputs and expected outputs to guide the model.
        """
        )

    # Template name
    template_name = st.text_input("Template Name", key="template_name")

    # Create tabs for each prompt component
    tabs = st.tabs(
        ["Context", "Instruction", "Response Format", "Constraints", "Examples"]
    )

    with tabs[0]:
        st.markdown("### Context")
        st.markdown("_Background information and role for the AI_")
        st.markdown(
            "Example: _You are an expert SQL developer helping to optimize database queries._"
        )
        context = st.text_area("Context", height=150, key="context")

    with tabs[1]:
        st.markdown("### Instruction")
        st.markdown("_The main task or request (required)_")
        st.markdown(
            "Example: _Review the following SQL query and suggest optimizations to improve its performance._"
        )
        instruction = st.text_area("Instruction", height=150, key="instruction")

    with tabs[2]:
        st.markdown("### Response Format")
        st.markdown("_How the response should be structured_")
        st.markdown(
            "Example: _Provide your suggestions in a numbered list, with each item explaining: 1) The issue identified, 2) Why it's a problem, 3) The recommended solution._"
        )
        response_format = st.text_area(
            "Response Format", height=150, key="response_format"
        )

    with tabs[3]:
        st.markdown("### Constraints")
        st.markdown("_Limitations or requirements for the response_")
        st.markdown(
            "Example: _Focus only on performance optimizations, not on syntax or style improvements. Limit your response to the top 3-5 most impactful changes._"
        )
        constraints = st.text_area("Constraints", height=150, key="constraints")

    with tabs[4]:
        st.markdown("### Examples")
        st.markdown("_Sample inputs and expected outputs_")

        # Initialize examples in session state if not present
        if "examples" not in st.session_state:
            st.session_state.examples = [{"query": "", "response": ""}]

        # Display existing examples
        for i, example in enumerate(st.session_state.examples):
            col1, col2, col3 = st.columns([0.45, 0.45, 0.1])

            with col1:
                st.text_area(
                    f"Input {i+1}",
                    value=example["query"],
                    key=f"example_query_{i}",
                    height=100,
                )

            with col2:
                st.text_area(
                    f"Expected Output {i+1}",
                    value=example["response"],
                    key=f"example_response_{i}",
                    height=100,
                )

            with col3:
                if st.button("🗑️", key=f"delete_example_{i}"):
                    st.session_state.examples.pop(i)
                    st.rerun()

        # Add new example button
        if st.button("Add Example"):
            st.session_state.examples.append({"query": "", "response": ""})
            st.rerun()

    # Preview section
    st.markdown("---")
    st.subheader("Preview")

    # Update examples from session state
    examples = []
    for i in range(len(st.session_state.examples)):
        query = st.session_state.get(f"example_query_{i}", "")
        response = st.session_state.get(f"example_response_{i}", "")
        if query or response:
            examples.append({"query": query, "response": response})

    # Create template for preview
    template = PromptTemplate(
        context=context,
        instruction=instruction,
        response_format=response_format,
        constraints=constraints,
        examples=examples,
    )

    # Show preview
    with st.expander("Full Prompt Preview", expanded=False):
        st.code(template.get_full_prompt(), language="markdown")

    # Save button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(
            "Save Template",
            type="primary",
            disabled=not template_name or not instruction,
        ):
            if "prompt_templates" not in st.session_state:
                st.session_state.prompt_templates = {}

            st.session_state.prompt_templates[template_name] = template
            st.session_state.lab.add_prompt_template(template, template_name)
            st.success(f"Template '{template_name}' saved successfully!")

    with col2:
        if st.button("Clear Form"):
            # Set the clear_form flag instead of directly modifying session state
            st.session_state.clear_form = True
            # We'll also set template_name to empty string in a way that doesn't conflict with the widget
            if "template_name" in st.session_state:
                del st.session_state["template_name"]
            st.rerun()

    # Sample Templates
    st.markdown("---")
    st.subheader("Load Sample Template")

    sample_templates = {
        "SQL Optimizer": {
            "context": "You are an expert SQL developer helping to optimize database queries.",
            "instruction": "Review the following SQL query and suggest optimizations to improve its performance.",
            "response_format": "Provide your suggestions in a numbered list, with each item explaining: 1) The issue identified, 2) Why it's a problem, 3) The recommended solution.",
            "constraints": "Focus only on performance optimizations, not on syntax or style improvements. Limit your response to the top 3-5 most impactful changes.",
            "examples": [
                {
                    "query": "SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id WHERE orders.date > '2023-01-01'",
                    "response": "1. Issue: Using SELECT *\n   Problem: Retrieving all columns increases I/O and network transfer.\n   Solution: Select only needed columns explicitly.\n\n2. Issue: Missing index on orders.date\n   Problem: The WHERE clause filters on a non-indexed column.\n   Solution: Add an index on orders.date for this common query pattern.",
                }
            ],
        },
        "Summarizer": {
            "context": "You are a professional content summarizer.",
            "instruction": "Summarize the following text while preserving the key information and main points.",
            "response_format": "Provide a concise summary in 2-3 paragraphs.",
            "constraints": "Maintain factual accuracy. Do not introduce information not present in the original text. Use simple, clear language.",
            "examples": [
                {
                    "query": 'Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.',
                    "response": "Artificial Intelligence (AI) refers to machines exhibiting intelligence, contrasting with the natural intelligence of humans and animals. The field focuses on studying intelligent agents—systems that perceive their surroundings and act to achieve goals effectively.\n\nWhile AI was once defined as machines mimicking human cognitive abilities like learning and problem-solving, modern AI researchers have shifted away from this anthropocentric definition. Instead, they conceptualize AI in terms of rationality and rational actions, which broadens the understanding of how intelligence can manifest beyond human-like characteristics.",
                }
            ],
        },
    }

    selected_template = st.selectbox(
        "Select a sample template", [""] + list(sample_templates.keys())
    )

    if selected_template and st.button("Load Selected Template"):
        # Instead of directly updating session state, set the load_template flag
        st.session_state.load_template = selected_template
        st.rerun()
