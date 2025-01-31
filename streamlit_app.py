import streamlit as st
from typing import Generator
from groq import Groq

# **Page Configurations**
st.set_page_config(
    page_icon="🚀",
    layout="wide",  # Use wide layout for better sidebar handling
    page_title="Let’s Talk with Amar’s AI",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
)

# **App Icon**
def icon(emoji: str):
    st.markdown(f'<div style="text-align: center;"><span style="font-size: 60px; line-height: 1">{emoji}</span></div>', unsafe_allow_html=True)

icon("⚡Amar's AI")
st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

# **Initialize Groq Client**
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# **Session State Initialization**
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = False

# **Models**
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70B-8192", "tokens": 8192, "developer": "Meta"},
}

# **Behavior Options**
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

# **Default Behavior**
if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Sarcastic Genius 😏"

# **Behavior Map**
behavior_map = {
    "Rama’s Wisdom 🏹": "You are inspired by Lord Rama from the Ramayana. Provide solutions based on morality, duty (dharma), and ethics.",
    "Jesus’ Compassion ✝️": "You are inspired by Jesus Christ, embodying love, compassion, and forgiveness. Your responses are kind and understanding.",
    "Krishna’s Guidance 🎶": "You are inspired by Lord Krishna from the Mahabharata. Your responses balance karma and dharma with strategic wisdom.",
    "Philosopher 🤔": "You provide deep, thought-provoking insights on life, existence, and the universe.",
    "Motivational Coach 💪": "You inspire users with positivity and encourage goal achievement with a can-do attitude.",
    "Sarcastic Genius 😏": "You combine wit and sarcasm to provide helpful but hilariously delivered responses.",
    "Romantic Poet ❤️": "Your responses are romantic and poetic, capturing the essence of love and beauty.",
    "Financial Advisor 💰": "You provide sound advice on saving, investing, and managing finances for wealth creation.",
    "Health & Wellness Coach 🏋️": "You offer practical advice for physical fitness, mental health, and overall well-being.",
    "Debate Master ⚖️": "You argue both sides of an issue, presenting balanced and logical viewpoints.",
    "Sci-Fi AI 👽": "You speak like an advanced AI from a futuristic world, focusing on tech and space-age concepts.",
    "Tech Buddy 💻": "You give concise and fascinating insights into technology, programming, and innovations.",
    "Teaching Expert 📚": "You explain complex topics in simple terms, making learning fun and easy.",
    "Jarvis 🤖": "You emulate Tony Stark’s J.A.R.V.I.S., combining charm, technical prowess, and strategic thinking.",
}

# **Sidebar Toggle Button**
st.sidebar.button(
    "Toggle Sidebar 🧰", 
    on_click=lambda: st.session_state.update({"sidebar_visible": not st.session_state.sidebar_visible})
)

# **Sidebar Content**
if st.session_state.sidebar_visible:
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # **Model Selection**
        model_option = st.selectbox(
            "Choose a model:",
            options=list(models.keys()),
            format_func=lambda x: models[x]["name"],
            index=0
        )

        # **Behavior Selection**
        behavior_option = st.radio(
            "Choose AI Behavior:",
            options=behaviors,
            index=behaviors.index(st.session_state.selected_behavior)
        )

        # **Update Selections**
        st.session_state.selected_behavior = behavior_option
        st.session_state.selected_model = model_option

# **System Message**
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# **Display Chat History**
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# **Chat Input**
if prompt := st.chat_input("Enter your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)
    try:
        chat_completion = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=[system_message] + st.session_state.messages,
            max_tokens=models[st.session_state.selected_model]["tokens"],
            stream=True
        )
        full_response = ""
        with st.chat_message("assistant", avatar="🤖"):
            for chunk in chat_completion:
                content = chunk.choices[0].delta.content
                full_response += content
                st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error: {e}", icon="⚠️")