import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.prompt_template import PromptTemplate


def show_test_prompt():
    """Display the test prompt page."""

    st.header("Test Your Prompt")

    # Educational content
    with st.expander("Why Test Prompts?", expanded=False):
        st.info(
            """
        Testing helps you understand how well your prompt performs across different inputs.
        It provides quantitative metrics to measure effectiveness rather than relying on
        subjective judgment.
        
        **Key Metrics:**
        - **Average Length**: Longer isn't always better, but too short may indicate incomplete answers
        - **Format Adherence**: How well the response follows your requested format
        - **Length Consistency**: How similar the response lengths are across different inputs
        """
        )

    # Select a prompt template
    if (
        "prompt_templates" not in st.session_state
        or not st.session_state.prompt_templates
    ):
        st.warning(
            "You haven't created any prompt templates yet. Go to the Create Prompt page to get started."
        )
        return

    template_name = st.selectbox(
        "Select a prompt template to test",
        options=list(st.session_state.prompt_templates.keys()),
    )

    template = st.session_state.prompt_templates[template_name]

    # Display template preview
    with st.expander("View Prompt Template", expanded=False):
        st.code(template.get_full_prompt(), language="markdown")

    # Test queries input
    st.subheader("Test Queries")
    st.markdown(
        "Enter queries to test your prompt against. Each query will be sent to the model."
    )

    # Initialize test queries in session state if not present
    if "test_queries" not in st.session_state:
        st.session_state.test_queries = [""]

    # Handle sample query selection (if set through the Use Sample button)
    if (
        "use_sample_query" in st.session_state
        and st.session_state.use_sample_query is not None
    ):
        sample_index, query = st.session_state.use_sample_query
        # Make sure we have enough query slots
        while len(st.session_state.test_queries) <= sample_index:
            st.session_state.test_queries.append("")
        # Update the test_queries list directly
        st.session_state.test_queries[sample_index] = query
        # Reset the sample selection
        st.session_state.use_sample_query = None

    # Display query inputs
    for i, query in enumerate(st.session_state.test_queries):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.text_area(f"Query {i+1}", value=query, key=f"query_{i}", height=100)
        with col2:
            if len(st.session_state.test_queries) > 1 and st.button(
                "🗑️", key=f"delete_query_{i}"
            ):
                st.session_state.test_queries.pop(i)
                st.rerun()

    # Add query button
    if st.button("Add Another Query"):
        st.session_state.test_queries.append("")
        st.rerun()

    # Model selection
    st.subheader("Model Settings")
    model = st.selectbox("Select model", options=["gemma3:4b"], index=0)

    # Run test button
    if st.button("Run Test", type="primary"):
        # Update queries from session state
        queries = []
        for i in range(len(st.session_state.test_queries)):
            query = st.session_state.get(f"query_{i}", "").strip()
            if query:
                queries.append(query)

        if not queries:
            st.error("Please enter at least one test query.")
            return

        # Show progress
        with st.spinner(f"Testing prompt with {model}..."):
            try:
                # Run the test
                lab = st.session_state.lab

                # Update model in tester
                lab.tester.model = model

                # Add template if not already in lab
                if template_name not in lab.prompt_templates:
                    lab.add_prompt_template(template, template_name)

                result = lab.test_prompt(template_name, queries)

                # Store result ID in session state for the results page
                if "test_results" not in st.session_state:
                    st.session_state.test_results = []

                if result["result_id"] not in st.session_state.test_results:
                    st.session_state.test_results.append(result["result_id"])

                st.success(f"Test completed! Result ID: {result['result_id']}")

                # Store as latest result for displaying
                st.session_state.latest_result = result
            except Exception as e:
                st.error(f"Error running test: {str(e)}")
                return

        # Display results summary
        st.subheader("Results Summary")

        # Add metrics explanation expander
        with st.expander("Understanding These Metrics", expanded=False):
            st.markdown(
                """
            These metrics help you evaluate how well your prompt is performing:
            
            ### Avg Length
            **What it measures:** The average number of characters in the responses generated by the model.
            
            **How it's calculated:** Total characters across all responses ÷ Number of test queries
            
            **Why it matters:** 
            - Longer responses often indicate more detailed answers
            - Very short responses might suggest insufficient detail
            - Very long responses could indicate verbosity
            - There's no universally "good" length — it depends on your specific needs
            
            ### Length Std Dev
            **What it measures:** The standard deviation of response lengths (consistency of length).
            
            **How it's calculated:** Statistical standard deviation of character counts across responses
            
            **Why it matters:**
            - Low values indicate consistent response lengths across different queries
            - High values show the model produces significantly different-sized responses
            - A value of 0.00 means all responses were exactly the same length
            - With only one test query, this will always be 0.00
            
            ### Format Adherence
            **What it measures:** How well the model followed your requested response format.
            
            **How it's calculated:** The percentage of responses that follow format indicators specified in your prompt
            
            **Why it matters:**
            - A value of 1.00 means perfect adherence to your requested format
            - Lower values indicate the model isn't consistently following your format instructions
            - If this value is low, consider making your format instructions more explicit or adding examples
            """
            )

        # Metrics
        metrics = result["results"]["metrics"]
        if metrics:
            cols = st.columns(len(metrics))
            for i, (metric, value) in enumerate(metrics.items()):
                with cols[i]:
                    st.metric(
                        label=metric.replace("_", " ").title(), value=f"{value:.2f}"
                    )
        else:
            st.info("No metrics available for this test.")

        # Sample responses
        st.subheader("Sample Responses")
        for i, resp in enumerate(result["results"]["responses"]):
            with st.expander(f"Query {i+1}", expanded=i == 0):
                st.markdown("**Query:**")
                st.code(resp["query"])

                st.markdown("**Response:**")
                st.code(
                    resp.get("response", "Error: " + resp.get("error", "Unknown error"))
                )

                st.markdown(
                    f"""
                **Metrics:**
                - Tokens: {resp.get('tokens_used', 'N/A')}
                - Response time: {resp.get('response_time', 'N/A'):.2f}s
                """
                )

        # Learning insights
        st.subheader("Improvement Suggestions")
        try:
            suggestions = lab.get_improvement_suggestions(result["result_id"])
            st.markdown(f"**{suggestions['summary']}**")

            for i, rec in enumerate(suggestions["recommendations"], 1):
                st.markdown(f"{i}. {rec}")
        except Exception as e:
            st.warning(f"Could not generate suggestions: {str(e)}")

    # Sample queries section
    st.markdown("---")
    st.subheader("Sample Queries")

    # Define sample queries dictionary
    sql_queries = [
        "SELECT * FROM products p JOIN order_items oi ON p.product_id = oi.product_id JOIN orders o ON oi.order_id = o.order_id WHERE o.customer_id = 123",
        "SELECT COUNT(*) FROM users WHERE last_login < DATE_SUB(NOW(), INTERVAL 30 DAY) AND account_status = 'active'",
    ]

    summarizer_queries = [
        "Climate change is the long-term alteration of temperature and typical weather patterns in a place. Climate change could refer to a particular location or the planet as a whole. Climate change may cause weather patterns to be less predictable. These unexpected weather patterns can make it difficult to maintain and grow crops in regions that rely on farming because expected temperature and rainfall levels can no longer be relied on. Climate change has also been connected with other damaging weather events such as more frequent and more intense hurricanes, floods, downpours, and winter storms.",
        'Machine learning is a branch of artificial intelligence (AI) and computer science which focuses on the use of data and algorithms to imitate the way that humans learn, gradually improving its accuracy. IBM has a rich history with machine learning. One of its own, Arthur Samuel, is credited for coining the term, "machine learning" with his research (PDF, 481 KB) (link resides outside IBM) around the game of checkers. Robert Nealey, the self-proclaimed checkers master, played the game on an IBM 7094 computer in 1962, and he lost to the computer. Compared to what can be done today, this feat seems trivial, but it\'s considered a major milestone in the field of artificial intelligence.',
    ]

    # Display sample queries based on template
    if template_name == "SQL Optimizer":
        queries_to_show = sql_queries
        st.write(f"Here are some sample queries for the SQL Optimizer template:")
    elif template_name == "Summarizer":
        queries_to_show = summarizer_queries
        st.write(f"Here are some sample queries for the Summarizer template:")
    else:
        queries_to_show = []

    # Show query samples if available
    for i, query in enumerate(queries_to_show):
        st.code(query)
        col1, col2 = st.columns([0.2, 0.8])
        with col1:
            if st.button(f"Use Sample {i+1}", key=f"use_sample_{i}"):
                # Store the selection in session state for handling at the beginning of the function
                st.session_state.use_sample_query = (i, query)
                st.rerun()
