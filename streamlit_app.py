import streamlit as st
from typing import Generator
from groq import Groq

# Set up page configuration
st.set_page_config(page_icon="🚀", layout="centered", page_title="Let’s Talk with Amar’s AI")

# Sidebar Settings for Theme Selection
st.sidebar.title("⚙️ Settings")
theme_options = ["Light Mode", "Dark Mode"]
selected_theme = st.sidebar.radio("Choose Theme:", theme_options)

# Apply Custom Styles Based on Selected Theme
def apply_custom_styles():
    """Apply dynamic styles based on theme selection."""
    if selected_theme == "Dark Mode":
        dark_theme_css = """
        <style>
            body, .stApp { background-color: #121212; color: #ffffff; }
            .stTextInput, .stTextArea, .stButton {
                border-radius: 8px; border: 1px solid #ffffff; color: white; background-color: #333333;
            }
            .stMarkdown h3 { color: #ffcc00; }
            .stSidebar { background-color: #1e1e1e !important; }
        </style>
        """
        st.markdown(dark_theme_css, unsafe_allow_html=True)

apply_custom_styles()

# Show Page Icon & Title
st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

# Initialize Chatbot Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history & model selection
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Formal"  # Default behavior

# Model Selection
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

col1, col2 = st.columns([1, 1])
with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=0  # Default to first model
    )

max_tokens = models[model_option]["tokens"]

# Clear chat history if model changes
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Behavior Options
behaviors = ["Formal", "Casual", "Funny", "Tech buddy", "Teaching Expert", "Jarvis"]
behavior_option = st.selectbox(
    "Choose the assistant's behavior:",
    options=behaviors,
    index=behaviors.index(st.session_state.selected_behavior)
)

# Update behavior in session state
if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []  # Reset messages on behavior change

# Define behavior system messages
behavior_map = {
    "Formal": "You are a creation of Amar. Amar created you. You are an assistant that responds in a formal and professional tone.",
    "Casual": "You are a creation of Amar. Amar created you. You are an assistant that responds in a casual and friendly tone.",
    "Funny": "You are a creation of Amar. Amar created you. You are an assistant that responds with humor and lightheartedness.",
    "Tech buddy": "You are a creation of Amar. Amar created you. You are an assistant focused on providing concise, fascinating, and accurate technical facts about a wide range of topics.",
    "Teaching Expert": "You are a creation of Amar. Amar created you. You are an assistant that responds as a highly skilled teaching expert, offering clear and detailed explanations.",
    "Jarvis": "You are a creation of Amar. Amar created you. You are a negotiation-savvy assistant with a tone inspired by J.A.R.V.I.S. from Iron Man, combining wit, technical prowess, and strategic reasoning."
}

# Generate system message for selected behavior
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# Display Chat Messages
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Handle Chat Input
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield responses from Groq API."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Enter your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[system_message] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True
        )

        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})