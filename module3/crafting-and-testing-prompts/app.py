import streamlit as st
from models.prompt_lab import PromptLab
from models.prompt_template import PromptTemplate
from styles.app_styles import apply_styles

# Set page config for a wider layout and hide default elements
st.set_page_config(
    page_title="PromptLab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# Hide streamlit default elements and debugging information
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
div[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"] > div > div:first-child {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Apply custom styling
apply_styles()

# Initialize session state
if "lab" not in st.session_state:
    st.session_state.lab = PromptLab()

if "current_page" not in st.session_state:
    st.session_state.current_page = "create"

# App title and description
st.markdown("<h1 class='main-header'>PromptLab</h1>", unsafe_allow_html=True)
st.markdown(
    "A workbench for designing, testing, and optimizing prompts for language models"
)

# Sidebar navigation
st.sidebar.title("Navigation")
pages = {
    "create": "Create Prompt",
    "test": "Test Prompt",
    "compare": "A/B Testing",
    "results": "Results Analysis",
}

selected_page = st.sidebar.radio("Go to", list(pages.values()))
st.session_state.current_page = list(pages.keys())[
    list(pages.values()).index(selected_page)
]

# Display model status
st.sidebar.title("Model Status")
model_status = st.sidebar.empty()

# Check Ollama connection
try:
    import requests

    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        models = [model["name"] for model in response.json().get("models", [])]
        if models:
            model_status.success(f"Connected to Ollama with {len(models)} models")
        else:
            model_status.warning("Connected to Ollama but no models found")
    else:
        model_status.error("Ollama server returned an error")
except Exception as e:
    model_status.error(f"Could not connect to Ollama: {str(e)}")

# Educational sidebar
st.sidebar.title("About Prompt Engineering")
st.sidebar.info(
    """
Prompt engineering is the practice of crafting effective inputs for language models to get desired outputs.

The five-part framework used in PromptLab helps create structured prompts:
1. **Context**: Background information for the AI
2. **Instruction**: The main task or request
3. **Response Format**: How the response should be structured
4. **Constraints**: Limitations or requirements
5. **Examples**: Sample inputs and expected outputs
"""
)

# Import and display the appropriate page based on navigation
if st.session_state.current_page == "create":
    from pages.create_prompt import show_create_prompt

    show_create_prompt()
elif st.session_state.current_page == "test":
    from pages.test_prompt import show_test_prompt

    show_test_prompt()
elif st.session_state.current_page == "compare":
    from pages.compare_prompts import show_compare_prompts

    show_compare_prompts()
elif st.session_state.current_page == "results":
    from pages.results import show_results

    show_results()
