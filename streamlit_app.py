import streamlit as st
from typing import Generator
from groq import Groq

# Set up page configuration
st.set_page_config(page_icon="🚀", layout="centered", page_title="Let’s Talk with Amar’s AI")

# Initialize session state for Theme Selection
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "Light Mode"  # Default Theme

# Sidebar Settings
st.sidebar.title("⚙️ Settings")

theme_options = ["Light Mode", "Dark Mode", "🌈 Rainbow Neon Mode"]
selected_theme = st.sidebar.radio("Choose Theme:", theme_options)

# Update session state
st.session_state.selected_theme = selected_theme

# Apply Custom Styles Based on Selected Theme
def apply_custom_styles():
    """Apply dynamic styles based on theme selection."""
    if st.session_state.selected_theme == "Dark Mode":
        dark_theme_css = """
        <style>
            body { background-color: #121212; color: #ffffff; }
            .stApp { background-color: #121212; }
            .stTextInput, .stTextArea, .stButton {
                border-radius: 8px; border: 1px solid #ffffff; color: white; background-color: #333333;
            }
            .stMarkdown h3 { color: #ffcc00; }
            .stSidebar { background-color: #1e1e1e !important; }
        </style>
        """
        st.markdown(dark_theme_css, unsafe_allow_html=True)

    elif st.session_state.selected_theme == "🌈 Rainbow Neon Mode":
        neon_theme_css = """
        <style>
            @keyframes rainbowBG {
                0% { background-color: #ff0000; }
                14% { background-color: #ff7300; }
                28% { background-color: #fffc00; }
                42% { background-color: #48ff00; }
                56% { background-color: #00ffc8; }
                70% { background-color: #0048ff; }
                84% { background-color: #7a00ff; }
                100% { background-color: #ff00d4; }
            }
            body, .stApp {
                animation: rainbowBG 10s linear infinite alternate;
                color: white;
            }
            .stTextInput, .stTextArea, .stButton {
                border-radius: 8px;
                border: 2px solid white;
                color: white;
                background: linear-gradient(45deg, #ff0000, #ff7300, #fffc00, #48ff00, #00ffc8, #0048ff, #7a00ff, #ff00d4);
                animation: rainbowBG 5s linear infinite alternate;
            }
            .stMarkdown h3 { text-shadow: 0px 0px 10px #ffffff; color: #fff; }
            .stSidebar { background-color: rgba(0, 0, 0, 0.8) !important; }
        </style>
        """
        st.markdown(neon_theme_css, unsafe_allow_html=True)

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

# Display Chat Messages
def chat_bubble(role, message):
    """Formats chat messages with styles based on theme."""
    if st.session_state.selected_theme == "🌈 Rainbow Neon Mode":
        return f"""
        <div style='background: linear-gradient(45deg, #ff0000, #ff7300, #fffc00, #48ff00, #00ffc8, #0048ff, #7a00ff, #ff00d4);
                    padding: 12px; border-radius: 10px; color: white; margin: 5px 0;
                    text-shadow: 0px 0px 10px #ffffff; font-weight: bold;'>
            🤖 <b>Amar's AI:</b> {message}
        </div>
        """
    elif role == "assistant":
        return f"""
        <div style='background-color: #007bff; padding: 10px; border-radius: 10px; color: white; margin: 5px 0;'>
            🤖 <b>Amar's AI:</b> {message}
        </div>
        """
    else:
        return f"""
        <div style='background-color: #333333; padding: 10px; border-radius: 10px; color: white; margin: 5px 0;'>
            👨‍💻 <b>You:</b> {message}
        </div>
        """

for message in st.session_state.messages:
    formatted_message = chat_bubble(message["role"], message["content"])
    st.markdown(formatted_message, unsafe_allow_html=True)

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
            messages=[{"role": "system", "content": "You are an assistant."}] + [
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
