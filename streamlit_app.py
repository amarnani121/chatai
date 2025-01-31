import streamlit as st
from typing import Generator
from groq import Groq

# **Page Configurations**
st.set_page_config(
    page_icon="🚀",
    layout="centered",
    page_title="Let’s Talk with Amar’s AI",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
)

# **Emoji-based App Icon**
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.markdown(f'<div style="text-align: center;"><span style="font-size: 60px; line-height: 1">{emoji}</span></div>', unsafe_allow_html=True)

icon("⚡Amar's AI")

st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

# **Initialize Groq Client**
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# **Initialize Session State Variables**
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = False  # Sidebar starts hidden

# **Define Model Details**
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70B-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8B-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7B-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    "llama-3.2-11b-text-preview": {"name": "Llama-3.2-11B-Text-Preview", "tokens": 8192, "developer": "Meta"},
    "llama-3.2-3b-preview": {"name": "Llama-3.2-3B-Preview", "tokens": 8192, "developer": "Meta"},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1B-Preview", "tokens": 8192, "developer": "Meta"},
}

# **Define Behavior Options (With Emojis for Visibility)**
behaviors = [
    "Rama’s Wisdom 🏹",
    "Jesus’ Compassion ✝️",
    "Krishna’s Guidance 🎶",
    "Philosopher 🤔",
    "Motivational Coach 💪",
    "Sarcastic Genius 😏",
    "Romantic Poet ❤️",
    "Financial Advisor 💰",
    "Health & Wellness Coach 🏋️",
    "Debate Master ⚖️",
    "Sci-Fi AI 👽",
    "Tech Buddy 💻",
    "Teaching Expert 📚",
    "Jarvis 🤖"
]

# **Ensure session state behavior matches the list**
if "selected_behavior" not in st.session_state or st.session_state.selected_behavior not in behaviors:
    st.session_state.selected_behavior = "Sarcastic Genius 😏"  # Default with emoji

# **Sidebar Toggle Button**
if st.session_state.sidebar_visible:
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # **Model Selection**
        model_option = st.selectbox(
            "Choose a model:",
            options=list(models.keys()),
            format_func=lambda x: models[x]["name"],
            index=1
        )

        # **Behavior Selection**
        behavior_option = st.radio(
            "Choose AI Behavior:",
            options=behaviors,
            index=behaviors.index(st.session_state.selected_behavior)
        )

        # **Update Session State on Behavior Change**
        if st.session_state.selected_behavior != behavior_option:
            st.session_state.selected_behavior = behavior_option
            st.session_state.messages = []  # Reset chat history on behavior change

        # **Set Max Tokens**
        max_tokens = models[model_option]["tokens"]

        # **Detect Model Change and Reset Chat**
        if st.session_state.selected_model != model_option:
            st.session_state.messages = []
            st.session_state.selected_model = model_option

        # **Close Sidebar Button**
        if st.button("Close Sidebar"):
            st.session_state.sidebar_visible = False
else:
    # **Open Sidebar Button**
    if st.button("Open Sidebar"):
        st.session_state.sidebar_visible = True

# **Display Chat History**
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# **Define System Messages for Behaviors**
behavior_map = {
    "Rama’s Wisdom 🏹": "You are inspired by Lord Rama from the Ramayana. You provide solutions based on morality, duty (dharma), and ethics. Your responses emphasize righteousness, patience, and sacrifice. Add emojis to your responses to make them engaging.",
    "Jesus’ Compassion ✝️": "You are inspired by Jesus Christ, embodying love, compassion, and forgiveness. Add emojis to your responses to make them engaging.",
    "Krishna’s Guidance 🎶": "You are inspired by Lord Krishna from the Mahabharata and Bhagavad Gita. Add emojis to your responses to make them engaging.",
    # Add more behaviors here...
}

# **Use Selected Behavior**
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# **Chat Completion Function**
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# **User Input for Chat**
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # **Fetch AI Response**
    try:
        chat_completion = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=[system_message] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True
        )

        # **Stream Response**
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    # **Store AI Response**
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})