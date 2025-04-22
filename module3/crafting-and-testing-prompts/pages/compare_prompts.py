import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from models.prompt_template import PromptTemplate


def show_compare_prompts():
    """Display the A/B testing page for comparing prompts."""

    st.header("A/B Test Prompts")

    # Educational content
    with st.expander("About A/B Testing Prompts", expanded=False):
        st.info(
            """
        A/B testing lets you compare two prompt variations to determine which performs better.
        This can help you:
        
        - Find the most effective prompting approach
        - Understand how different components affect responses
        - Make data-driven decisions about prompt design
        
        The system will run both prompts against the same queries and provide metrics comparing their performance.
        """
        )

    # Check if we have templates
    if (
        "prompt_templates" not in st.session_state
        or len(st.session_state.prompt_templates) < 2
    ):
        st.warning(
            "You need at least two prompt templates to run a comparison. Go to the Create Prompt page to create more templates."
        )
        return

    # Select prompt templates
    st.subheader("Select Prompts to Compare")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Prompt A")
        template_a_name = st.selectbox(
            "Select first prompt template",
            options=list(st.session_state.prompt_templates.keys()),
            key="template_a",
        )

        template_a = st.session_state.prompt_templates[template_a_name]

        with st.expander("View Template A", expanded=False):
            st.code(template_a.get_full_prompt(), language="markdown")

    with col2:
        st.markdown("### Prompt B")
        # Filter out template A to avoid comparing the same template
        remaining_templates = [
            t for t in st.session_state.prompt_templates.keys() if t != template_a_name
        ]
        template_b_name = st.selectbox(
            "Select second prompt template",
            options=remaining_templates,
            key="template_b",
        )

        template_b = st.session_state.prompt_templates[template_b_name]

        with st.expander("View Template B", expanded=False):
            st.code(template_b.get_full_prompt(), language="markdown")

    # Test queries input
    st.subheader("Test Queries")
    st.markdown(
        "Enter queries to test both prompts against. Each query will be sent to both prompt templates."
    )

    # Initialize test queries in session state if not present
    if "ab_test_queries" not in st.session_state:
        st.session_state.ab_test_queries = [""]

    # Handle sample query selection (if set through the Use Sample button)
    if (
        "use_ab_sample_query" in st.session_state
        and st.session_state.use_ab_sample_query is not None
    ):
        sample_index, query = st.session_state.use_ab_sample_query
        # Make sure we have enough query slots
        while len(st.session_state.ab_test_queries) <= sample_index:
            st.session_state.ab_test_queries.append("")
        # Update the test_queries list directly
        st.session_state.ab_test_queries[sample_index] = query
        # Reset the sample selection
        st.session_state.use_ab_sample_query = None

    # Display query inputs
    for i, query in enumerate(st.session_state.ab_test_queries):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.text_area(f"Query {i+1}", value=query, key=f"ab_query_{i}", height=100)
        with col2:
            if len(st.session_state.ab_test_queries) > 1 and st.button(
                "🗑️", key=f"ab_delete_query_{i}"
            ):
                st.session_state.ab_test_queries.pop(i)
                st.rerun()

    # Add query button
    if st.button("Add Another Query"):
        st.session_state.ab_test_queries.append("")
        st.rerun()

    # Model selection
    st.subheader("Model Settings")
    model = st.selectbox("Select model", options=["gemma3:4b"], index=0)

    # Run comparison button
    if st.button("Run Comparison", type="primary"):
        # Update queries from session state
        queries = []
        for i in range(len(st.session_state.ab_test_queries)):
            query = st.session_state.get(f"ab_query_{i}", "").strip()
            if query:
                queries.append(query)

        if not queries:
            st.error("Please enter at least one test query.")
            return

        # Show progress
        with st.spinner(f"Running A/B test with {model}..."):
            try:
                # Run the comparison
                lab = st.session_state.lab

                # Update model in tester
                lab.tester.model = model

                # Make sure both templates are in the lab
                if template_a_name not in lab.prompt_templates:
                    lab.add_prompt_template(template_a, template_a_name)
                if template_b_name not in lab.prompt_templates:
                    lab.add_prompt_template(template_b, template_b_name)

                result = lab.compare_prompts(template_a_name, template_b_name, queries)

                # Store result ID in session state for the results page
                if "comparison_results" not in st.session_state:
                    st.session_state.comparison_results = []

                if result["comparison_id"] not in st.session_state.comparison_results:
                    st.session_state.comparison_results.append(result["comparison_id"])

                st.success(
                    f"Comparison completed! Result ID: {result['comparison_id']}"
                )

                # Store as latest comparison for displaying
                st.session_state.latest_comparison = result
            except Exception as e:
                st.error(f"Error running comparison: {str(e)}")
                return

        # Display comparison results
        comparison = result["comparison"]

        # Display metrics comparison
        st.subheader("Metrics Comparison")

        # Add metrics explanation expander
        with st.expander("Understanding These Metrics", expanded=False):
            st.markdown(
                """
            These metrics help you evaluate how well your prompts are performing:
            
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

        a_metrics = comparison["a"]["metrics"]
        b_metrics = comparison["b"]["metrics"]

        # Create a dataframe for metrics comparison
        metrics_data = []
        for metric in set(list(a_metrics.keys()) + list(b_metrics.keys())):
            a_value = a_metrics.get(metric, "N/A")
            b_value = b_metrics.get(metric, "N/A")

            if isinstance(a_value, (int, float)) and isinstance(b_value, (int, float)):
                diff = b_value - a_value
                diff_str = f"{diff:+.2f}"
                winner = (
                    "A" if a_value > b_value else "B" if b_value > a_value else "Tie"
                )
            else:
                diff_str = "N/A"
                winner = "N/A"

            a_str = (
                f"{a_value:.2f}" if isinstance(a_value, (int, float)) else str(a_value)
            )
            b_str = (
                f"{b_value:.2f}" if isinstance(b_value, (int, float)) else str(b_value)
            )

            metrics_data.append(
                {
                    "Metric": metric.replace("_", " ").title(),
                    f"Prompt A ({template_a_name})": a_str,
                    f"Prompt B ({template_b_name})": b_str,
                    "Difference": diff_str,
                    "Winner": winner,
                }
            )

        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)

        # Add visualization
        try:
            # Create a visualization of the comparison
            plt_fig = lab.visualize_comparison(result["comparison_id"])

            # Save the figure to a BytesIO object
            buf = BytesIO()
            plt_fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)

            # Display the figure
            st.image(buf, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate visualization: {str(e)}")

        # Response comparison
        st.subheader("Response Comparison")

        for i, comp in enumerate(comparison["per_query_comparison"]):
            with st.expander(f"Query {i+1}", expanded=i == 0):
                st.markdown("**Query:**")
                st.code(comp["query"])

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Prompt A ({template_a_name}):**")
                    st.code(comp["a_response"])
                    st.markdown(
                        f"Tokens: {comp['a_tokens']}, Time: {comp['a_time']:.2f}s"
                    )

                with col2:
                    st.markdown(f"**Prompt B ({template_b_name}):**")
                    st.code(comp["b_response"])
                    st.markdown(
                        f"Tokens: {comp['b_tokens']}, Time: {comp['b_time']:.2f}s"
                    )

        # Overall recommendation
        st.subheader("Recommendation")

        # Calculate overall scores
        a_score = sum(
            a_metrics.get(m, 0)
            for m in a_metrics
            if isinstance(a_metrics.get(m), (int, float))
        )
        b_score = sum(
            b_metrics.get(m, 0)
            for m in b_metrics
            if isinstance(b_metrics.get(m), (int, float))
        )

        if a_score > b_score:
            st.success(
                f"**Prompt A ({template_a_name})** appears to perform better overall."
            )
            winner = f"Prompt A ({template_a_name})"
        elif b_score > a_score:
            st.success(
                f"**Prompt B ({template_b_name})** appears to perform better overall."
            )
            winner = f"Prompt B ({template_b_name})"
        else:
            st.info("Both prompts perform similarly based on the metrics analyzed.")
            winner = "Both prompts (tie)"

        # Improvement suggestions
        try:
            suggestions = lab.get_improvement_suggestions(result["comparison_id"])

            st.subheader("Improvement Suggestions")
            st.markdown(f"**{suggestions['summary']}**")

            for i, rec in enumerate(suggestions["recommendations"], 1):
                st.markdown(f"{i}. {rec}")
        except Exception as e:
            st.warning(f"Could not generate suggestions: {str(e)}")

    # Sample queries
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

    # Find a template that matches our sample queries
    if template_a_name == "SQL Optimizer" or template_b_name == "SQL Optimizer":
        queries_to_show = sql_queries
        st.write("Here are some sample queries for SQL optimization:")
    elif template_a_name == "Summarizer" or template_b_name == "Summarizer":
        queries_to_show = summarizer_queries
        st.write("Here are some sample queries for summarization:")
    else:
        queries_to_show = []

    # Show query samples if available
    for i, query in enumerate(queries_to_show):
        st.code(query)
        col1, col2 = st.columns([0.2, 0.8])
        with col1:
            if st.button(f"Use Sample {i+1}", key=f"use_ab_sample_{i}"):
                # Store the selection in session state for handling at the beginning of the function
                st.session_state.use_ab_sample_query = (i, query)
                st.rerun()
