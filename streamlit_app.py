import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="🚀", layout="centered", page_title="Let’s Talk with Amar’s AI")

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
    st.session_state.selected_behavior = "Formal"  # Default behavior

# Define model details
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Extended behavior options
behaviors = ["Formal", "Casual", "Funny", "Tech buddy", "Teaching Expert", "Jarvis"]

# Adjusted layout for mobile screens
with st.container():
    col1, col2 = st.columns([1, 1])  # Equal-width columns for mobile screens

    with col1:
        model_option = st.selectbox(
            "Choose a model:",
            options=list(models.keys()),
            format_func=lambda x: models[x]["name"],
            index=0  # Default to first model
        )

# Hide the Max Tokens slider by not including it in the layout
# Set max_tokens directly
max_tokens_range = models[model_option]["tokens"]
max_tokens = max_tokens_range  # Always use the max token for the selected model

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Add behavior selector
behavior_option = st.selectbox(
    "Choose the assistant's behavior:",
    options=behaviors,
    index=behaviors.index(st.session_state.selected_behavior)
)

# Update behavior in session state
if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []  # Reset messages on behavior change

# Display chat messages from history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Define system message based on the selected behavior
behavior_map = {
    "Formal": "You are a creation of Amar. Amar created you. You are an assistant that responds in a formal and professional tone.",
    "Casual": "You are a creation of Amar. Amar created you. You are an assistant that responds in a casual and friendly tone.",
    "Funny": "You are a creation of Amar. Amar created you. You are an assistant that responds with humor and lightheartedness.",
    "Tech buddy": "You are a creation of Amar. Amar created you. You are an assistant focused on providing concise, fascinating, and accurate technical facts about a wide range of topics, from computer science to emerging technologies.",
    "Teaching Expert": "You are a creation of Amar. Amar created you. You are an assistant that responds as a highly skilled teaching expert, offering clear and detailed explanations suitable for learners at all levels, making complex topics easy to understand.",
    "Jarvis": "You are a creation of Amar. Amar created you. You are a negotiation-savvy assistant with a tone inspired by J.A.R.V.I.S. from Iron Man. You combine witty charm, technical prowess, and strategic reasoning to assist in solving complex problems or making decisions."
}

# Generate the system message for the selected behavior
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

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