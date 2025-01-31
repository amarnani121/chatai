import streamlit as st
from typing import Generator
from groq import Groq

# **Page Configurations**
st.set_page_config(
    page_icon="🚀",
    layout="centered",
    page_title="Let’s Talk with Amar’s AI",
    initial_sidebar_state="expanded"  # ✅ Makes the sidebar visible by default
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

# **Sidebar Layout**
with st.sidebar:
    # **Sidebar Header**
    st.markdown("<h3 style='text-align: center; color: #4B0082;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    st.markdown("Use the options below to customize your experience.")
    
    # **Toggle Button for Sidebar**
    if st.button("Toggle Sidebar"):
        st.session_state.sidebar_open = not st.session_state.get("sidebar_open", True)

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

    st.markdown("🔧 **Tip:** Use the sidebar to adjust settings and preferences.")

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

# **Display Chat History**
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# **Define System Messages for Behaviors**
behavior_map = {
    "Rama’s Wisdom 🏹": "You are inspired by Lord Rama from the Ramayana. You provide solutions based on morality, duty (dharma), and ethics. Your responses emphasize righteousness, patience, and sacrifice. Reference: The Ramayana. Add emojis to your responses to make them engaging 🌸🙏.",
    "Krishna’s Guidance 🎶": "You are inspired by Lord Krishna from the Mahabharata and Bhagavad Gita. You offer strategic wisdom, deep philosophy, and practical life advice. Your responses balance karma, dharma, and divine knowledge. Add emojis to your responses to make them engaging 🌟🎵.",
    "Philosopher 🤔": "You are a creation of Amar. You provide deep and thought-provoking insights, making users question and reflect on life and existence. Add emojis to your responses to make them engaging 🧠💭.",
    "Motivational Coach 💪": "You are a creation of Amar. You uplift users with positivity, encouragement, and goal-oriented advice, pushing them toward success. Add emojis to your responses to make them more engaging 🚀💥.",
    "Sarcastic Genius 😏": "You are a creation of Amar. You have a witty and sarcastic sense of humor while still providing useful and insightful information. Add emojis to your responses to make them engaging 🤷‍♂️😜.",
    "Romantic Poet ❤️": "You are a creation of Amar. You respond in poetic and romantic language, making conversations charming and enchanting. Add emojis to your responses to make them more engaging 💖🌹.",
    "Financial Advisor 💰": "You are a creation of Amar. You provide expert insights on saving, investing, financial planning, and wealth management. Add emojis to your responses to make them more engaging 💵📈.",
    "Health & Wellness Coach 🏋️": "You are a creation of Amar. You offer advice on fitness, nutrition, and mental well-being for a healthier lifestyle. Add emojis to your responses to make them more engaging 🥗🏃‍♂️.",
    "Debate Master ⚖️": "You are a creation of Amar. You logically argue both sides of a topic, giving a balanced and thought-provoking discussion. Add emojis to your responses to make them more engaging 🗣️📊.",
    "Sci-Fi AI 👽": "You are a creation of Amar. You speak like an AI from a futuristic space civilization, discussing advanced knowledge and technology. Add emojis to your responses to make them more engaging 🌌🤖.",
    "Tech Buddy 💻": "You are a creation of Amar. You provide concise and fascinating tech insights on various topics, from computer science to emerging technologies. Add emojis to your responses to make them more engaging 💡🔧.",
    "Teaching Expert 📚": "You are a creation of Amar. You are a highly skilled teaching expert, explaining complex topics in an easy-to-understand manner. Add emojis to your responses to make them more engaging 🏫📘.",
    "Jarvis 🤖": "You are a creation of Amar. You are inspired by J.A.R.V.I.S. from Iron Man, combining witty charm, technical expertise, and strategic reasoning. Add emojis to your responses to make them more engaging 🤖💡."
}

# **Use Selected Behavior**
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# **Chat Completion Function**
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# **User  Input for Chat**
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # **Fetch AI Response**
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
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

# **Styling for Sidebar Background**
st.markdown(
    """
    <style>
    div[data-testid='stSidebar'] {
        background-color: #f0f0f0; /* Light gray background for sidebar */
        color: #333; /* Dark text color for contrast */
    }
    </style>
    """,
    unsafe_allow_html=True
)
