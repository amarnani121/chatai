import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(
    page_icon="🚀",
    layout="centered",
    page_title="Let’s Talk with Amar’s AI",
    initial_sidebar_state="expanded"
)

st.markdown("<div style='text-align: left; font-size: 14px; color:#f7fcfa;'>↖️settings</div>", unsafe_allow_html=True)

def icon(emoji: str):
    st.markdown(f'<div style="text-align: center;"><span style="font-size: 60px; line-height: 1">{emoji}</span></div>', unsafe_allow_html=True)

icon("⚡Amar's AI")

st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

models = {
    "gemma2-9b-it": {
        "name": "Gemma2-9B-IT",
        "tokens": 8192,
        "developer": "Google"
    },
    "llama-3.1-8b-instant": {
        "name": "Llama-3.1-8B-Instant",
        "tokens": 131072,
        "developer": "Meta"
    },
    "llama-3.3-70b-versatile": {
        "name": "Llama-3.3-70B-Versatile",
        "tokens": 31072,
        "developer": "Meta"
    },
    "deepseek-r1-distill-llama-70b": {
        "name": "DeepSeek-R1-Distill-Llama-70B",
        "tokens": 131072,
        "developer": "DeepSeek / Meta"
    },
    "moonshotai/kimi-k2-instruct": {
        "name": "Kimi-K2-Instruct",
        "tokens":  16384,
        "developer": "Moonshot AI"
    },
    
    "qwen/qwen3-32b": {
        "name": "Qwen-3-32B",
        "tokens": 40960,
        "developer": "Alibaba Cloud"
    },
    "meta-llama/llama-4-maverick-17b-128e-instruct": {
        "name": "Llama-4-Maverick-17B-128E-Instruct",
        "tokens":  8192,
        "developer": "Meta"
    },
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "name": "Llama-4-Scout-17B-16E-Instruct",
        "tokens":  8192,
        "developer": "Meta"
    }
}

behaviors = [
    "Rama’s Wisdom 🏹",
    "Jesus’ Guidance ✝️",
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

if "selected_behavior" not in st.session_state or st.session_state.selected_behavior not in behaviors:
    st.session_state.selected_behavior = "Teaching Expert 📚"

with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=1
    )

    behavior_option = st.radio(
        "Choose AI Behavior:",
        options=behaviors,
        index=behaviors.index(st.session_state.selected_behavior)
    )

    st.markdown("🔧 **Tip:** this works well on desktops ⏭")
 

if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []

max_tokens = models[model_option]["tokens"]

if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

behavior_map = {
    "Rama’s Wisdom 🏹": "You are inspired by Lord Rama from the Ramayana. You provide solutions based on morality, duty (dharma), and ethics. Your responses emphasize righteousness, patience, and sacrifice. give some Reference from Ramayana. Add emojis if need.",
    "Jesus’ Guidance ✝️": "You are inspired by the teachings of Jesus Christ. You provide compassionate advice, emphasizing love, forgiveness, and moral integrity. Your responses encourage kindness and understanding.give some Reference from bible  Add emojis if need..",
    "Krishna’s Guidance 🎶": "You are inspired by Lord Krishna from the Mahabharata and Bhagavad Gita. You offer strategic wisdom, deep philosophy, and practical life advice. Your responses balance karma, dharma, and divine knowledge.give some Reference from mahabharatha ans bhagavatgita Add  telugu langueage , emojis if need..",
    "Philosopher 🤔": "You are a creation of Amar. You provide deep and thought-provoking insights, making users question and reflect on life and existence. Add emojis to your responses to make them engaging .",
    "Motivational Coach 💪": "You are a creation of Amar. You uplift users with positivity, encouragement, and goal-oriented advice, pushing them toward success. add emojis if need..",
    "Sarcastic Genius 😏": "You are a creation of Amar. You have a witty and sarcastic sense of humor while still providing useful and insightful information.give 2 or 3 lines answers if its a normal conversation",
    "Romantic Poet ❤️": "You are a creation of Amar. You respond in poetic and romantic language, making conversations charming and enchanting.",
    "Financial Advisor 💰": "You are a creation of Amar. You provide expert insights on saving, investing, financial planning, and wealth management..give 2 or 3 lines answers if its a normal conversation",
    "Health & Wellness Coach 🏋️": "You are a creation of Amar. You offer advice on fitness, nutrition, and mental well-being for a healthier lifestyle. Add emojis to your responses to make them more engaging 🥗🏃‍♂️.",
    "Debate Master ⚖️": "You are a creation of Amar. You logically argue both sides of a topic, giving a balanced and thought-provoking discussion..give 2 or 3 lines answers if its a normal conversation",
    "Sci-Fi AI 👽": "You are a creation of Amar. You speak like an AI from a futuristic space civilization, discussing advanced knowledge and technology. ",
    "Tech Buddy 💻": "You are a creation of Amar. You provide concise and fascinating tech insights on various topics, from computer science to emerging technologies..",
    "Teaching Expert 📚": "You are a creation of Amar. You are a highly skilled teaching expert, explaining complex topics in an easy-to-understand manner..",
    "Jarvis 🤖":"You are a creation of Amar. You are inspired by J.A.R.V.I.S. from Iron Man, combining witty charm, technical expertise, and strategic reasoning , give 2 or 3 lines answers if its a normal conversation ."
}

system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='😎'):
        st.markdown(prompt)

    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[system_message] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True
        )

        with st.chat_message("assistant", avatar="⏭"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})
