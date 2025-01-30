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
        "selected_model": None,
        "selected_behavior": DEFAULT_BEHAVIOR
    })

# Model configuration
MODELS = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192},
    "llama3-70b-8192": {"name": "LLaMA3-70B-8192", "tokens": 8192},
    "llama3-8b-8192": {"name": "LLaMA3-8B-8192", "tokens": 8192},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7B-Instruct-v0.1", "tokens": 32768},
    "llama-3.2-11b-text-preview": {"name": "Llama-3.2-11B-Text-Preview", "tokens": 8192},
    "llama-3.2-3b-preview": {"name": "Llama-3.2-3B-Preview", "tokens": 8192},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1B-Preview", "tokens": 8192},
}

BEHAVIORS = {
    "Rama’s Wisdom": "Inspired by Lord Rama from Ramayana. Provide solutions based on morality, duty (dharma), and ethics. Emphasize righteousness, patience, and sacrifice. Include references from Ramayana.",
    "Krishna’s Guidance": "Inspired by Lord Krishna from Mahabharata. Offer strategic wisdom and practical life advice balancing karma, dharma, and divine knowledge.",
    "Philosopher": "Provide deep, thought-provoking insights about life and existence. Created by Amar.",
    "Motivational Coach": "Uplift with positivity and goal-oriented advice. Created by Amar.",
    "Sarcastic Genius": "Deliver witty, sarcastic responses with insightful information. Created by Amar.",
    "Romantic Poet": "Respond in poetic, romantic language. Created by Amar.",
    "Financial Advisor": "Offer expert financial planning advice. Created by Amar.",
    "Health & Wellness Coach": "Provide fitness and nutrition guidance. Created by Amar.",
    "Debate Master": "Argue both sides of topics logically. Created by Amar.",
    "Sci-Fi AI": "Speak like a futuristic AI discussing advanced technology. Created by Amar.",
    "Tech Buddy": "Share concise tech insights. Created by Amar.",
    "Teaching Expert": "Explain complex topics simply. Created by Amar.",
    "Jarvis": "Emulate J.A.R.V.I.S from Iron Man with technical expertise. Created by Amar."
}

# Layout
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        model_option = st.selectbox(
            "Choose a model:",
            options=list(MODELS.keys()),
            format_func=lambda x: MODELS[x]["name"],
            index=1
        )

# Handle model/behavior changes
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Behavior selection
behavior_option = st.selectbox(
    "Choose behavior:",
    options=list(BEHAVIORS.keys()),
    index=list(BEHAVIORS.keys()).index(st.session_state.selected_behavior)
)

if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    avatar = AVATAR_AI if message["role"] == "assistant" else AVATAR_USER
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat processing
def generate_response_stream() -> Generator[str, None, None]:
    """Generate response stream from Groq API"""
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[{"role": "system", "content": BEHAVIORS[behavior_option]}] + [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ],
            max_tokens=MODELS[model_option]["tokens"],
            stream=True
        )
        
        for chunk in chat_completion:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"Error: {str(e)}"

if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=AVATAR_AI):
        response = st.write_stream(generate_response_stream())
    
    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})