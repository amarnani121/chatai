import streamlit as st
from typing import Generator
from groq import Groq
import time
import json

# **🔹 Streamlit Page Config (Sidebar opens first)**
st.set_page_config(page_icon="🚀", layout="wide", page_title="Let’s Talk with Amar’s AI", initial_sidebar_state="expanded")

# **🔹 Sidebar UI (Better Visibility)**
with st.sidebar:
    st.title("⚙️ AI Settings")  # More visible sidebar title
    
    # Model Selection
    st.subheader("🤖 Choose a Model")
    models = {
        "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
        "llama3-70b-8192": {"name": "LLaMA3-70B-8192", "tokens": 8192, "developer": "Meta"},
        "llama3-8b-8192": {"name": "LLaMA3-8B-8192", "tokens": 8192, "developer": "Meta"},
        "mixtral-8x7b-32768": {"name": "Mixtral-8x7B-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
        "llama-3.2-11b-text-preview": {"name": "Llama-3.2-11B-Text-Preview", "tokens": 8192, "developer": "Meta"},
    }
    model_option = st.selectbox("Select a model:", options=list(models.keys()), format_func=lambda x: models[x]["name"])

    # Behavior Selection (Teaching Expert Default)
    st.subheader("🎭 AI Behaviors")
    behaviors = [
        "Rama’s Wisdom", "Krishna’s Guidance", "Philosopher", "Motivational Coach",
        "Sarcastic Genius", "Romantic Poet", "Financial Advisor", "Health & Wellness Coach",
        "Debate Master", "Sci-Fi AI", "Tech Buddy", "Teaching Expert", "Jarvis"
    ]

    if "selected_behavior" not in st.session_state:
        st.session_state.selected_behavior = "Teaching Expert"  # Default Behavior

    behavior_option = st.radio("Choose behavior:", behaviors, index=behaviors.index(st.session_state.selected_behavior))

    # Save Model & Behavior Selection
    st.session_state.selected_model = model_option
    st.session_state.selected_behavior = behavior_option

    # **🔹 Clear Chat Button**
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = []

    # **🔹 Chat Export Button**
    if st.session_state.get("messages"):
        chat_history = json.dumps(st.session_state.messages, indent=4)
        st.download_button("📥 Export Chat", chat_history, "chat_history.json", "application/json")

# **🔹 Main Chat Interface**
st.title("🚀 Chat with Amar’s AI")

# Chat history storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# **🔹 AI Behavior Mapping**
behavior_map = {
    "Rama’s Wisdom": "You are inspired by Lord Rama from the Ramayana. You provide moral and ethical solutions. Add references from Ramayana and use engaging emojis.",
    "Krishna’s Guidance": "You offer strategic wisdom inspired by Krishna from the Bhagavad Gita. Responses should balance karma, dharma, and divine knowledge.",
    "Philosopher": "You provide deep and thought-provoking insights, making users question life and existence.",
    "Motivational Coach": "You uplift users with positivity, encouragement, and goal-oriented advice.",
    "Sarcastic Genius": "You have a witty and sarcastic sense of humor while providing useful information.",
    "Romantic Poet": "You respond in poetic and romantic language, making conversations enchanting.",
    "Financial Advisor": "You provide expert insights on saving, investing, and financial planning.",
    "Health & Wellness Coach": "You offer advice on fitness, nutrition, and mental well-being.",
    "Debate Master": "You logically argue both sides of a topic for balanced discussions.",
    "Sci-Fi AI": "You speak like an AI from a futuristic space civilization, discussing advanced technology.",
    "Tech Buddy": "You provide concise and fascinating tech insights on various topics.",
    "Teaching Expert": "You are a skilled teaching expert, explaining complex topics in an easy-to-understand manner.",
    "Jarvis": "You are inspired by J.A.R.V.I.S., combining witty charm, technical expertise, and strategic reasoning."
}

# **🔹 System Message for AI**
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

# **🔹 Function to Stream AI Responses**
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# **🔹 Typing Indicator Effect**
def simulate_typing():
    with st.chat_message("assistant", avatar="🤖"):
        typing_message = st.empty()
        dots = ""
        for _ in range(3):
            dots += "."
            typing_message.markdown(f"🤖 *Typing{dots}*")
            time.sleep(0.5)
        typing_message.empty()

# **🔹 Chat Input Handling**
if prompt := st.chat_input("Enter your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    simulate_typing()  # Show typing effect

    # **🔹 Fetch AI Response**
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[system_message] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=models[model_option]["tokens"],
            stream=True
        )

        # **Stream AI Response**
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(f"🚨 Error: {e}")

    # **🔹 Save AI Response**
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})