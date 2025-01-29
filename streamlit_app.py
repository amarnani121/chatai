import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="🚀", layout="wide", page_title="Let’s Talk with Amar’s AI")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.markdown(f'<div style="text-align: center;"><span style="font-size: 60px; line-height: 1">{emoji}</span></div>', unsafe_allow_html=True)

icon("⚡Amar's AI")

st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Rama’s Wisdom"  # Default behavior

# Define model details
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70B-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8B-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7B-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    "llama-3.2-11b-text-preview": {"name": "Llama-3.2-11B-Text-Preview", "tokens": 8192, "developer": "Meta"},
    "llama-3.2-3b-preview": {"name": "Llama-3.2-3B-Preview", "tokens": 8192, "developer": "Meta"},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1B-Preview", "tokens": 8192, "developer": "Meta"},
}

# Updated behavior options (removed 'Formal')
behaviors = [
    "Rama’s Wisdom",
    "Krishna’s Guidance",
    "Philosopher",
    "Motivational Coach",
    "Sarcastic Genius",
    "Romantic Poet",
    "Financial Advisor",
    "Health & Wellness Coach",
    "Debate Master",
    "Sci-Fi AI",
    "Tech Buddy",
    "Teaching Expert",
    "Jarvis"
]

# Layout for model selection on left side
col1, col2 = st.columns([1, 3])  # Adjust the ratio of the columns
with col1:
    st.markdown("<h4>Select Model and Behavior</h4>", unsafe_allow_html=True)
    
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=1,
        key="model",
        help="Select your preferred model for the conversation"
    )
    
    behavior_option = st.selectbox(
        "Choose the assistant's behavior:",
        options=behaviors,
        index=behaviors.index(st.session_state.selected_behavior),
        key="behavior",
        help="Select the behavior of the assistant"
    )

# Layout for the chat on the right side
with col2:
    st.markdown("<h3 style='text-align: center;'>Chat with Amar's AI 🚀</h3>", unsafe_allow_html=True)

    # Set max_tokens directly
    max_tokens = models[model_option]["tokens"]

    # Detect model change and clear chat history
    if st.session_state.selected_model != model_option:
        st.session_state.messages = []
        st.session_state.selected_model = model_option

    # Add behavior selector
    if st.session_state.selected_behavior != behavior_option:
        st.session_state.selected_behavior = behavior_option
        st.session_state.messages = []  # Reset messages on behavior change

    # Display chat messages from history
    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Generate the system message for the selected behavior
    system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

    if prompt := st.chat_input("Enter your prompt here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar='👨‍💻'):
            st.markdown(prompt)

        # Fetch response from Groq API
        try:
            chat_completion = client.chat.completions.create(
                model=model_option,
                messages=[system_message] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ],
                max_tokens=max_tokens,
                stream=True
            )

            # Use the generator function with st.write_stream
            with st.chat_message("assistant", avatar="🤖"):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)

        except Exception as e:
            st.error(e, icon="🚨")

        # Append the full response to session_state.messages
        if isinstance(full_response, str):
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
        else:
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": combined_response}
            )