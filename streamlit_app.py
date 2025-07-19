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
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70B-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8B-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7B-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    "llama-3.2-11b-text-preview": {"name": "Llama-3.2-11B-Text-Preview", "tokens": 8192, "developer": "Meta"},
    "llama-3.2-3b-preview": {"name": "Llama-3.2-3B-Preview", "tokens": 8192, "developer": "Meta"},
    "llama-3.2-1b-preview": {"name": "Llama-3.2-1B-Preview", "tokens": 8192, "developer": "Meta"},
    "distil-whisper-large-v3-en": {"name": "distil-whisper-large-v3-en", "tokens": 8192, "developer": "Hugging Face"},
    "llama-3.1-8b-instant": {"name": "Llama-3.1-8B-Instant", "tokens": 131072, "developer": "Meta"},
    "llama-3.3-70b-versatile": {"name": "Llama-3.3-70B-Versatile", "tokens": 131072, "developer": "Meta"},
    "meta-llama/llama-guard-4-12b": {"name": "Meta-Llama/Guard-4-12B", "tokens": 131072, "developer": "Meta"},
    "whisper-large-v3": {"name": "Whisper-Large-V3", "tokens": 8192, "developer": "OpenAI"},
    "whisper-large-v3-turbo": {"name": "Whisper-Large-V3-Turbo", "tokens": 8192, "developer": "OpenAI"},
    "deepseek-r1-distill-llama-70b": {"name": "DeepSeek-R1-Distill-Llama-70B", "tokens": 131072, "developer": "DeepSeek / Meta"},
    "meta-llama/llama-4-maverick-17b-128e-instruct": {"name": "Llama-4-Maverick-17B-128E-Instruct", "tokens": 131072, "developer": "Meta"},
    "meta-llama/llama-4-scout-17b-16e-instruct": {"name": "Llama-4-Scout-17B-16E-Instruct", "tokens": 131072, "developer": "Meta"},
    "meta-llama/llama-prompt-guard-2-22m": {"name": "Llama-Prompt-Guard-2-22M", "tokens": 512, "developer": "Meta"},
    "meta-llama/llama-prompt-guard-2-86m": {"name": "Llama-Prompt-Guard-2-86M", "tokens": 512, "developer": "Meta"},
    "mistral-saba-24b": {"name": "Mistral-Saba-24B", "tokens": 32768, "developer": "Mistral AI"},
    "moonshotai/kimi-k2-instruct": {"name": "Kimi-K2-Instruct", "tokens": 131072, "developer": "Moonshot AI"},
    "playai-tts": {"name": "PlayAI-TTS", "tokens": 8192, "developer": "PlayAI"},
    "playai-tts-arabic": {"name": "PlayAI-TTS-Arabic", "tokens": 8192, "developer": "PlayAI"},
    "qwen/qwen3-32b": {"name": "Qwen-3-32B", "tokens": 131072, "developer": "Alibaba Cloud"},
    "llava-v1.5-7b-4096-preview": {"name": "LLaVA-­V1.5-­7B (Vision‑preview)", "tokens": 4096, "developer": "Meta"}
}

# Select Model
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=1
    )

max_tokens = models[model_option]["tokens"]

if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

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
            messages=[{"role": "system", "content": "You are Amar's AI, helpful and fast."}] + [
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
