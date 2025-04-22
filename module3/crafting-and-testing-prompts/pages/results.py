import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from models.prompt_template import PromptTemplate


def show_results():
    """Display the results analysis page."""

    st.header("Results Analysis")

    # Educational content
    with st.expander("About Results Analysis", expanded=False):
        st.info(
            """
        This page allows you to review and analyze the results of your prompt tests and comparisons.
        
        The metrics captured can help you:
        - Understand how well prompts meet your requirements
        - Compare different prompt variations objectively
        - Make data-driven decisions about prompt design
        
        You can view detailed reports, charts, and improvement suggestions to help refine your prompts.
        """
        )

    # Check if we have any results
    if (
        not hasattr(st.session_state, "test_results")
        or not st.session_state.test_results
    ) and (
        not hasattr(st.session_state, "comparison_results")
        or not st.session_state.comparison_results
    ):
        st.warning(
            "You haven't run any tests or comparisons yet. Go to the Test Prompt or A/B Testing pages to generate results."
        )
        return

    # Create tabs for single tests and comparisons
    tabs = st.tabs(["Prompt Tests", "A/B Comparisons"])

    # Single Tests Tab
    with tabs[0]:
        if (
            not hasattr(st.session_state, "test_results")
            or not st.session_state.test_results
        ):
            st.info(
                "No prompt test results available. Go to the Test Prompt page to test a template."
            )
        else:
            st.subheader("Select Test Result")
            result_id = st.selectbox(
                "Choose a test result to view",
                options=st.session_state.test_results,
                format_func=lambda x: x.split("_")[0]
                + " (v"
                + x.split("_")[1][1:]
                + ")",
            )

            if result_id:
                # Generate and display the report
                try:
                    lab = st.session_state.lab
                    report = lab.generate_report(result_id)

                    # Display the report using Streamlit's markdown
                    st.markdown(report)

                    # Get the full result data
                    result = lab.test_results[result_id]

                    # Show metrics in a more visual way
                    st.subheader("Metrics Visualization")

                    # Create a bar chart for metrics
                    if result["metrics"]:
                        fig, ax = plt.subplots(figsize=(10, 5))
                        metrics = {
                            k.replace("_", " ").title(): v
                            for k, v in result["metrics"].items()
                        }

                        # Sort metrics by value
                        sorted_metrics = dict(
                            sorted(
                                metrics.items(), key=lambda item: item[1], reverse=True
                            )
                        )

                        names = list(sorted_metrics.keys())
                        values = list(sorted_metrics.values())

                        # Create bar chart
                        bars = ax.bar(names, values, color="steelblue")

                        # Add value labels on top of bars
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(
                                bar.get_x() + bar.get_width() / 2.0,
                                height + 0.01,
                                f"{height:.2f}",
                                ha="center",
                                va="bottom",
                            )

                        plt.xticks(rotation=45, ha="right")
                        plt.tight_layout()

                        # Convert to image for Streamlit
                        buf = BytesIO()
                        plt.savefig(buf, format="png")
                        buf.seek(0)
                        st.image(buf, use_container_width=True)

                    # Improvement suggestions
                    st.subheader("Improvement Suggestions")
                    try:
                        suggestions = lab.get_improvement_suggestions(result_id)
                        st.markdown(f"**{suggestions['summary']}**")

                        for i, rec in enumerate(suggestions["recommendations"], 1):
                            st.markdown(f"{i}. {rec}")
                    except Exception as e:
                        st.warning(
                            f"Could not generate improvement suggestions: {str(e)}"
                        )

                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")

    # A/B Comparisons Tab
    with tabs[1]:
        if (
            not hasattr(st.session_state, "comparison_results")
            or not st.session_state.comparison_results
        ):
            st.info(
                "No comparison results available. Go to the A/B Testing page to compare templates."
            )
        else:
            st.subheader("Select Comparison Result")

            # Format the comparison IDs to be more readable
            def format_comparison_id(comp_id):
                parts = comp_id.split("_")
                if parts[0] == "compare" and len(parts) >= 4:
                    return f"{parts[1]} vs {parts[3]}"
                return comp_id

            comparison_id = st.selectbox(
                "Choose a comparison result to view",
                options=st.session_state.comparison_results,
                format_func=format_comparison_id,
            )

            if comparison_id:
                # Generate and display the report
                try:
                    lab = st.session_state.lab
                    report = lab.generate_report(comparison_id)

                    # Display the report using Streamlit's markdown
                    st.markdown(report)

                    # Add visualization
                    st.subheader("Metrics Visualization")
                    try:
                        # Create a visualization of the comparison
                        plt_fig = lab.visualize_comparison(comparison_id)

                        # Save the figure to a BytesIO object
                        buf = BytesIO()
                        plt_fig.savefig(buf, format="png", bbox_inches="tight")
                        buf.seek(0)

                        # Display the figure
                        st.image(buf, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not generate visualization: {str(e)}")

                    # Get the full comparison data
                    comparison = lab.test_results[comparison_id]

                    # Improvement suggestions
                    st.subheader("Improvement Suggestions")
                    try:
                        suggestions = lab.get_improvement_suggestions(comparison_id)
                        st.markdown(f"**{suggestions['summary']}**")

                        for i, rec in enumerate(suggestions["recommendations"], 1):
                            st.markdown(f"{i}. {rec}")
                    except Exception as e:
                        st.warning(
                            f"Could not generate improvement suggestions: {str(e)}"
                        )

                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")

    # Export section
    st.markdown("---")
    st.subheader("Export Results")

    export_format = st.radio(
        "Select export format",
        options=["Markdown Report", "JSON Data"],
        horizontal=True,
    )

    if st.button("Export Selected Result"):
        # Get the currently active tab and selected result
        active_tab = 0 if tabs[0]._active else 1

        if (
            active_tab == 0
            and hasattr(st.session_state, "test_results")
            and st.session_state.test_results
        ):
            result_id = st.session_state.get(
                "selected_test_result", st.session_state.test_results[0]
            )
            try:
                lab = st.session_state.lab

                if export_format == "Markdown Report":
                    report = lab.generate_report(result_id)
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"prompt_test_{result_id}.md",
                        mime="text/markdown",
                    )
                else:  # JSON Data
                    import json

                    result_data = lab.test_results[result_id]
                    json_data = json.dumps(result_data, indent=2)
                    st.download_button(
                        label="Download JSON Data",
                        data=json_data,
                        file_name=f"prompt_test_{result_id}.json",
                        mime="application/json",
                    )
            except Exception as e:
                st.error(f"Error exporting result: {str(e)}")

        elif (
            active_tab == 1
            and hasattr(st.session_state, "comparison_results")
            and st.session_state.comparison_results
        ):
            comparison_id = st.session_state.get(
                "selected_comparison", st.session_state.comparison_results[0]
            )
            try:
                lab = st.session_state.lab

                if export_format == "Markdown Report":
                    report = lab.generate_report(comparison_id)
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"comparison_{comparison_id}.md",
                        mime="text/markdown",
                    )
                else:  # JSON Data
                    import json

                    comparison_data = lab.test_results[comparison_id]
                    json_data = json.dumps(comparison_data, indent=2)
                    st.download_button(
                        label="Download JSON Data",
                        data=json_data,
                        file_name=f"comparison_{comparison_id}.json",
                        mime="application/json",
                    )
            except Exception as e:
                st.error(f"Error exporting comparison: {str(e)}")
        else:
            st.warning("No result selected to export.")
