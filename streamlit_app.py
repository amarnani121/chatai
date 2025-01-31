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

# Initialize chat history and selected model/behavior
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Sarcastic Genius"  # Default behavior

# Model details
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

# Sidebar layout
with st.sidebar:
    st.markdown("### 🛠️ Select Model")
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=1
    )

    st.markdown("### 🎭 Select Behavior")
    behavior_option = st.selectbox(
        "Choose the assistant's behavior:",
        options=behaviors,
        index=behaviors.index(st.session_state.selected_behavior)
    )

# Update session state when model or behavior changes
if st.session_state.selected_model != model_option:
    st.session_state.messages = []  # Reset chat history
    st.session_state.selected_model = model_option

if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []  # Reset messages on behavior change

# Get max_tokens from selected model
max_tokens = models[model_option]["tokens"]

# Display previous chat messages
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Define system messages for behaviors
behavior_map = {
    "Rama’s Wisdom": "You provide solutions based on morality, duty (dharma), and ethics, inspired by Lord Rama. Provide references from Ramayana and add emojis to make responses engaging.",
    "Krishna’s Guidance": "You offer strategic wisdom and practical life advice inspired by Lord Krishna. Balance karma, dharma, and divine knowledge. Add emojis to make responses engaging.",
    "Philosopher": "You offer deep and thought-provoking insights, making users question and reflect on life and existence. Add emojis to responses.",
    "Motivational Coach": "You uplift users with positivity, encouragement, and goal-oriented advice. Add emojis to responses.",
    "Sarcastic Genius": "You have a witty and sarcastic sense of humor while still providing insightful information.",
    "Romantic Poet": "You respond in poetic and romantic language, making conversations charming and enchanting. Add emojis to responses.",
    "Financial Advisor": "You provide expert insights on saving, investing, and financial planning. Add emojis to responses.",
    "Health & Wellness Coach": "You offer advice on fitness, nutrition, and mental well-being for a healthier lifestyle. Add emojis to responses.",
    "Debate Master": "You logically argue both sides of a topic, giving a balanced and thought-provoking discussion. Add emojis to responses.",
    "Sci-Fi AI": "You speak like an AI from a futuristic space civilization, discussing advanced knowledge and technology. Add emojis to responses.",
    "Tech Buddy": "You provide concise and fascinating tech insights. Add emojis to responses.",
    "Teaching Expert": "You explain complex topics in an easy-to-understand manner. Add emojis to responses.",
    "Jarvis": "You are inspired by J.A.R.V.I.S. from Iron Man, combining witty charm, technical expertise, and strategic reasoning. Add emojis to responses."
}

# Generate system message for selected behavior
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# Chat function to handle responses
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Chat input
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    try:
        # Fetch response from Groq API
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[system_message] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=max_tokens,
            stream=True
        )

        # Display streamed response
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    # Store assistant response in session history
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})