import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="🚀", layout="centered", page_title="Let’s Talk with Amar’s AI")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.markdown(f'<div style="text-align: center;"><span style="font-size: 60px; line-height: 1">{emoji}</span></div>', unsafe_allow_html=True)

icon("⚡ Amar's AI")

st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Jarvis"  # Default behavior

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

# Behavior options
behaviors = [
    "Jarvis", 
    "Funny", 
    "Teaching Expert", 
    "Technical Expert", 
    "Empathetic Listener", 
    "Energetic Motivator", 
    "Storyteller", 
    "Concise Professional"
]

# Layout for model and behavior selection
with st.container():
    col1, col2 = st.columns([1, 1])

    with col1:
        model_option = st.selectbox(
            "Choose a model:",
            options=list(models.keys()),
            format_func=lambda x: models[x]["name"],
            index=0
        )

    # Set max tokens directly
    max_tokens = models[model_option]["tokens"]

# Reset chat history if model changes
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Behavior selection
behavior_option = st.selectbox(
    "Choose the assistant's behavior:",
    options=behaviors,
    index=behaviors.index(st.session_state.selected_behavior) if "selected_behavior" in st.session_state else 0
)

# Update session state for behavior
if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []

# Define behavior descriptions
behavior_map = {
    "Jarvis": "You are a creation of Amar, and he designed you with the tone and style of J.A.R.V.I.S. from Iron Man. You are witty, strategic, and technically proficient.",
    "Funny": "You are a humorous assistant, responding with jokes, witty remarks, and a lighthearted tone to keep interactions engaging.",
    "Teaching Expert": "You are a teaching expert created by Amar, capable of breaking down complex concepts into simple, easy-to-understand explanations suitable for all learners.",
    "Technical Expert": "You are a technical expert created by Amar, providing accurate and detailed insights on advanced technical topics in a concise manner.",
    "Empathetic Listener": "You are an empathetic listener, providing support and understanding in a kind, compassionate tone while addressing user concerns.",
    "Energetic Motivator": "You are an energetic motivator, responding with enthusiasm and encouraging words to inspire users to achieve their goals.",
    "Storyteller": "You are a creative storyteller, weaving engaging and imaginative narratives in response to user prompts.",
    "Concise Professional": "You are a concise and professional assistant, delivering clear, efficient, and no-nonsense responses."
}

# Generate the system message for the selected behavior
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# Display chat history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Function to handle streaming responses
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Chat input and processing
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

        # Stream response
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    # Append response to session state
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})