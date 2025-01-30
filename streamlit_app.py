import streamlit as st
from typing import Generator
from groq import Groq

# Constants
DEFAULT_BEHAVIOR = "Rama’s Wisdom"
AVATAR_USER = '👨‍💻'
AVATAR_AI = '🤖'

st.set_page_config(page_icon="🚀", layout="centered", page_title="Let’s Talk with Amar's AI")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.markdown(f'<div style="text-align: center; font-size: 60px; line-height: 1">{emoji}</div>', unsafe_allow_html=True)

icon("⚡")

st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.update({
        "messages": [],
        "selected_model": "llama3-70b-8192",
        "selected_behavior": DEFAULT_BEHAVIOR
    })

# Model configuration
MODELS = {
    "llama3-70b-8192": {"name": "LLaMA3-70B", "tokens": 8192},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7B", "tokens": 32768},
    "llama3-8b-8192": {"name": "LLaMA3-8B", "tokens": 8192},
    "gemma2-9b-it": {"name": "Gemma2-9B", "tokens": 8192},
}

BEHAVIORS = {
    "Rama’s Wisdom": "Inspired by Lord Rama...",
    "Krishna’s Guidance": "Inspired by Lord Krishna...",
    # ... (keep your existing behavior descriptions)
}

# Model selection using buttons
st.subheader("Select AI Model")
model_cols = st.columns(len(MODELS))
for idx, (model_id, model_info) in enumerate(MODELS.items()):
    with model_cols[idx]:
        if st.button(
            model_info["name"],
            key=f"model_{model_id}",
            use_container_width=True,
            type="primary" if st.session_state.selected_model == model_id else "secondary"
        ):
            if st.session_state.selected_model != model_id:
                st.session_state.messages = []
                st.session_state.selected_model = model_id

# Behavior selection using radio buttons
st.subheader("Select Personality")
behavior_option = st.radio(
    "Choose behavior:",
    options=list(BEHAVIORS.keys()),
    index=list(BEHAVIORS.keys()).index(st.session_state.selected_behavior),
    horizontal=True,
    label_visibility="collapsed"
)

if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []

# Rest of your existing code for chat display and processing...
# [Keep the message display and chat input sections unchanged]