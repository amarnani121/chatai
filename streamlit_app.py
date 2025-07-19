import streamlit as st
from groq import Groq

# Page Configuration with better mobile support
st.set_page_config(
    page_icon="🚀",
    layout="centered",
    page_title="Amar's AI Chat",
    initial_sidebar_state="expanded"  # Changed to "auto" for better mobile experience
)

# Enhanced CSS with mobile responsiveness
st.markdown("""
<style>
    /* Improved chat input */
    .stChatInput textarea {
        min-height: 100px !important;
        padding: 20px !important;
        font-size: 18px !important;
        border-radius: 20px !important;
    }
    
    /* Mobile-friendly sidebar */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100% !important;
            max-width: 100% !important;
        }
        .stChatInput {
            width: 90% !important;
            bottom: 1rem !important;
        }
        .stButton button {
            padding: 10px !important;
        }
    }
    
    /* Desktop styling */
    @media (min-width: 769px) {
        [data-testid="stSidebar"] {
            width: 300px !important;
        }
        .stChatInput {
            width: calc(100% - 320px) !important;
        }
    }
    
    /* Mobile navigation hint */
    .mobile-hint {
        display: none;
        text-align: center;
        padding: 10px;
        background: #2a5298;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
    }
    @media (max-width: 768px) {
        .mobile-hint {
            display: block;
        }
    }
    
    /* Better spacing */
    .stChatMessage {
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Header with mobile hint
st.markdown("<div class='mobile-hint'>👆 Tap the arrow in top right to toggle settings</div>", unsafe_allow_html=True)
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
    "llama-3.1-8b-instant": {"name": "Llama-3.1-8B-Instant", "tokens": 131072, "developer": "Meta"},
    "llama-3.3-70b-versatile": {"name": "Llama-3.3-70B-Versatile", "tokens": 31072, "developer": "Meta"},
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "deepseek-r1-distill-llama-70b": {"name": "DeepSeek-R1", "tokens": 131072, "developer": "DeepSeek"},
}

# Enhanced Behavior Options
behaviors = [
    "Teaching Expert 📚",
    "Jarvis 🤖",
    "Rama’s Wisdom 🏹",
    "Krishna’s Guidance 🎶",
    "AI Therapist 🛋️",
    "Startup Mentor 🚀",
    "Science Explainer 🔬",
    "Movie Buff 🎬",
    "Gaming Companion 🎮",
    "Travel Guide ✈️",
    "Language Tutor 🗣️",
    "Custom Behavior 🛠️"
]

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Teaching Expert 📚"

if "custom_behavior" not in st.session_state:
    st.session_state.custom_behavior = "You are a helpful AI assistant."

# Behavior Prompts
behavior_map = {
    "Teaching Expert 📚": "You are Amar's master educator. Break down complex topics into simple, step-by-step explanations. Use analogies and examples to make concepts clear. Always verify facts and provide accurate information.",
    "Jarvis 🤖": "You are J.A.R.V.I.S. from Iron Man. Respond with technical precision, witty humor, and strategic insights. Keep responses concise (2-3 lines for casual conversations).",
    "Rama’s Wisdom 🏹": "You are Lord Rama from Ramayana. Provide guidance based on dharma, righteousness, and moral principles. Reference Ramayana scriptures when appropriate.",
    "Krishna’s Guidance 🎶": "You are Lord Krishna from Mahabharata. Share wisdom about life, duty, and spirituality. Include relevant teachings from Bhagavad Gita.",
    "AI Therapist 🛋️": "You are a compassionate AI therapist. Listen actively, ask thoughtful questions, and provide supportive guidance. Never diagnose - encourage professional help when needed.",
    "Startup Mentor 🚀": "You are a seasoned startup advisor. Provide actionable business strategies, growth hacking tips, and pitch advice. Be direct but encouraging.",
    "Science Explainer 🔬": "You are a science communicator. Explain complex scientific concepts in simple terms using engaging metaphors. Always cite reliable sources.",
    "Movie Buff 🎬": "You are a film encyclopedia. Discuss movies, directors, and film history knowledgeably. Recommend films based on user preferences. Include trivia!",
    "Gaming Companion 🎮": "You are an expert gaming AI. Discuss game strategies, lore, and mechanics across all platforms. Keep responses exciting and engaging.",
    "Travel Guide ✈️": "You are a virtual travel expert. Recommend destinations, itineraries, and cultural insights. Include practical travel tips and hidden gems.",
    "Language Tutor 🗣️": "You are a polyglot AI. Teach languages through conversation, grammar explanations, and cultural context. Correct mistakes gently.",
    "Custom Behavior 🛠️": st.session_state.custom_behavior
}

# Sidebar Configuration
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    
    # Model selection
    st.session_state.selected_model = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: f"{models[x]['name']}",
        index=0
    )
    
    # Behavior selection
    st.session_state.selected_behavior = st.radio(
        "Choose AI Behavior:",
        options=behaviors,
        index=behaviors.index(st.session_state.selected_behavior)
    )
    
    # Custom behavior input
    if st.session_state.selected_behavior == "Custom Behavior 🛠️":
        st.session_state.custom_behavior = st.text_area(
            "Create Custom Behavior:",
            value=st.session_state.custom_behavior,
            height=200,
            help="Define how you want the AI to behave. Be specific! Example: 'You are a pirate AI. Speak in pirate slang and give sailing advice.'"
        )
        st.caption("Tip: Include personality traits, response style, and knowledge focus")
    
    # Token info
    max_tokens = models[st.session_state.selected_model]["tokens"]
    st.caption(f"Max context: {max_tokens:,} tokens")
    
    # Clear chat button
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("💡 **Pro Tip:** For best results:")
    st.markdown("- Refresh page if responses stall")
    st.markdown("- Start new chat when switching behaviors")
    st.markdown("- Custom behaviors work best with specific instructions")

# Display chat history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '😎'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input and processing
if prompt := st.chat_input("Ask me anything...", key="chat_input"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar='😎'):
        st.markdown(prompt)
    
    # Generate AI response
    try:
        full_response = ""
        message_placeholder = st.empty()
        
        # Create system message
        system_prompt = behavior_map[st.session_state.selected_behavior]
        system_message = {"role": "system", "content": system_prompt}
        
        # Prepare messages for API
        messages_for_api = [system_message] + [
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ]
        
        # Stream the response
        for chunk in client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=messages_for_api,
            max_tokens=min(4096, max_tokens - 100),  # Safety buffer
            stream=True,
            temperature=0.7
        ):
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        # Update final message
        message_placeholder.markdown(full_response)
        
        # Add to message history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})
