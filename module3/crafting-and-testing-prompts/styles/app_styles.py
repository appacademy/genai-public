def apply_styles():
    """Apply custom styling to the Streamlit app."""
    import streamlit as st

    # Custom CSS
    st.markdown(
        """
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4257B2;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5C7AEA;
    }
    .info-box {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
