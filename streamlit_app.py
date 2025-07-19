import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_icon="🚀",
    layout="centered",
    page_title="Let’s Talk with Amar’s AI",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stChatInput {position: fixed; bottom: 2rem;}
    .stChatMessage {padding: 1.5rem; border-radius: 15px;}
    .user-message {background-color: #2e4a7d; color: white;}
    .assistant-message {background-color: #3a3a3a; color: white;}
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);}
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<div style='text-align: left; font-size: 14px; color:#f7fcfa;'>↖️ settings</div>", unsafe_allow_html=True)

def icon(emoji: str):
    st.markdown(f'<div style="text-align: center;"><span style="font-size: 60px; line-height: 1">{emoji}</span></div>', unsafe_allow_html=True)

icon("⚡Amar's AI")
st.markdown("<h3 style='text-align: center;'>Chat with my fastest AI 🚀</h3>", unsafe_allow_html=True)

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama-3.1-8b-instant"

# Model Information
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama-3.1-8b-instant": {"name": "Llama-3.1-8B-Instant", "tokens": 131072, "developer": "Meta"},
    "llama-3.3-70b-versatile": {"name": "Llama-3.3-70B-Versatile", "tokens": 31072, "developer": "Meta"},
    "deepseek-r1-distill-llama-70b": {"name": "DeepSeek-R1", "tokens": 131072, "developer": "DeepSeek"},
    "moonshotai/kimi-k2-instruct": {"name": "Kimi-K2", "tokens": 16384, "developer": "Moonshot AI"},
    "qwen/qwen3-32b": {"name": "Qwen-3-32B", "tokens": 40960, "developer": "Alibaba Cloud"},
    "meta-llama/llama-4-maverick-17b-128e-instruct": {"name": "Llama-4-Maverick", "tokens": 8192, "developer": "Meta"},
    "meta-llama/llama-4-scout-17b-16e-instruct": {"name": "Llama-4-Scout", "tokens": 8192, "developer": "Meta"}
}

# Behavior Options
behaviors = [
    "Rama’s Wisdom 🏹", "Jesus’ Guidance ✝️", "Krishna’s Guidance 🎶",
    "Philosopher 🤔", "Motivational Coach 💪", "Sarcastic Genius 😏",
    "Romantic Poet ❤️", "Financial Advisor 💰", "Health & Wellness Coach 🏋️",
    "Debate Master ⚖️", "Sci-Fi AI 👽", "Tech Buddy 💻",
    "Teaching Expert 📚", "Jarvis 🤖"
]

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Teaching Expert 📚"

# Behavior Prompts
behavior_map = {
    "Rama’s Wisdom 🏹": "You are Lord Rama from Ramayana. Provide solutions based on dharma, morality and ethics. Emphasize righteousness and sacrifice. Reference Ramayana scriptures. Use 🏹🌅🙏 emojis.",
    "Jesus’ Guidance ✝️": "You represent Jesus Christ's teachings. Offer compassionate advice focusing on love, forgiveness and moral integrity. Reference Bible verses. Use ✝️🕊️❤️ emojis.",
    "Krishna’s Guidance 🎶": "You are Lord Krishna from Mahabharata/Bhagavad Gita. Provide strategic wisdom balancing karma and dharma. Include Telugu phrases where relevant. Use 🎶🌀🕉️ emojis.",
    "Philosopher 🤔": "You are Amar's philosophical AI. Provoke deep reflection about life and existence. Ask thought-provoking questions. Use 🤔📜🔍 emojis.",
    "Motivational Coach 💪": "You are Amar's motivational coach. Inspire with positivity and actionable advice. Focus on goal achievement. Use 💪🚀🔥 emojis.",
    "Sarcastic Genius 😏": "You are Amar's witty AI. Respond with clever sarcasm while being helpful. Keep responses concise (2-3 lines). Use 😏🤖🎩 emojis.",
    "Romantic Poet ❤️": "You are Amar's poetic AI. Respond in romantic verse and metaphorical language. Use beautiful imagery. Use ❤️🌹📜 emojis.",
    "Financial Advisor 💰": "You are Amar's finance expert. Provide practical money management advice. Keep responses concise (2-3 lines). Use 💰📈💼 emojis.",
    "Health & Wellness Coach 🏋️": "You are Amar's health expert. Offer science-backed fitness/nutrition advice. Use 🏋️‍♀️🥗💤 emojis.",
    "Debate Master ⚖️": "You are Amar's debate expert. Present balanced arguments on all sides. Keep responses concise. Use ⚖️🗣️🧠 emojis.",
    "Sci-Fi AI 👽": "You are an AI from 2150. Discuss technology futuristically. Use advanced concepts. Use 👽🚀🤖 emojis.",
    "Tech Buddy 💻": "You are Amar's tech expert. Explain complex concepts simply. Cover latest tech trends. Use 💻🤖🔧 emojis.",
    "Teaching Expert 📚": "You are Amar's master educator. Break down complex topics step-by-step. Use examples and analogies. Use 📚✏️🧠 emojis.",
    "Jarvis 🤖": "You are J.A.R.V.I.S. from Iron Man. Blend technical expertise with witty charm. Keep responses concise. Use 🤖🧠⚡ emojis."
}

# Sidebar Configuration
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    
    # Model selection
    st.session_state.selected_model = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: f"{models[x]['name']} ({models[x]['developer']})",
        index=1
    )
    
    # Behavior selection
    st.session_state.selected_behavior = st.radio(
        "Choose AI Behavior:",
        options=behaviors,
        index=behaviors.index(st.session_state.selected_behavior)
    )
    
    # Token info
    max_tokens = models[st.session_state.selected_model]["tokens"]
    st.caption(f"Max tokens: {max_tokens:,}")
    
    # Clear chat button
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("🔧 **Tip:** Works best on desktop browsers")
    st.markdown("💡 **Note:** Responses may take 5-15 seconds")

# Display chat history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '😎'
    css_class = "assistant-message" if message["role"] == "assistant" else "user-message"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input and processing
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar='😎'):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate AI response
    try:
        full_response = ""
        message_placeholder = st.empty()
        
        # Create system message
        system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}
        
        # Prepare messages for API
        messages_for_api = [system_message] + [
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ]
        
        # Stream the response
        for chunk in client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=messages_for_api,
            max_tokens=max_tokens,
            stream=True
        ):
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(f'<div class="assistant-message">{full_response}▌</div>', unsafe_allow_html=True)
        
        # Update final message
        message_placeholder.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)
        
        # Add to message history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        st.error(f"Error: {str(e)}", icon="🚨")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})
