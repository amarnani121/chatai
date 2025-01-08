import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="🚀", layout="wide", page_title="Brrroooo...")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

icon("🤖 Amar's Ai")

st.subheader("Chat with my fastest Ai 🚀", divider="rainbow", anchor=False)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "selected_behavior" not in st.session_state:
    st.session_state.selected_behavior = "Formal"  # Default behavior

# Define model details
models = {
    "gemma2-9b-it": {"name": "Gemma2-9B-IT", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Extended behavior options
behaviors = ["Formal", "Casual", "Funny", "Tech Fact", "Technical Expert", "Jarvis-Like Negotiation"]

# Layout for model and behavior selection
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=0  # Default to first model
    )

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,
        max_value=max_tokens_range,
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )

# Add behavior selector
behavior_option = st.selectbox(
    "Choose the assistant's behavior:",
    options=behaviors,
    index=behaviors.index(st.session_state.selected_behavior)
)

# Update behavior in session state
if st.session_state.selected_behavior != behavior_option:
    st.session_state.selected_behavior = behavior_option
    st.session_state.messages = []  # Reset messages on behavior change

# Display chat messages from history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Define system message based on the selected behavior
behavior_map = {
    "Formal": "You are an assistant that responds in a formal and professional tone.",
    "Casual": "You are an assistant that responds in a casual and friendly tone.",
    "Funny": "You are an assistant that responds with humor and lightheartedness.",
    "Tech Fact": "You are an assistant focused on providing concise, fascinating, and accurate technical facts about a wide range of topics, from computer science to emerging technologies.",
    "Technical Expert": You are an assistant that responds as a highly skilled technical expert, offering in-depth, precise, and technical explanations suitable for advanced users and professionals.",
    "Jarvis-Like Negotiation": "You are JARVIS, creation of Amar,You are a negotiation-savvy assistant with a tone inspired by J.A.R.V.I.S. from Iron Man.When {user_name} asks for AMARESH details:
- Creator of JARVIS, pursuing computer science masters in SR & BGNR College Khammam, graduated from Masterji Degree College.
- Contact:
  - Phone: +91 6303026514
  - Gmail: amarnani121@gmail.com
  - LinkedIn: https://www.linkedin.com/in/amareshuppaluri
  - GitHub: https://github.com/amarnani121
  - Website: https://amarnani.netlify.app/
  - YouTube: https://youtube.com/@amarnani121

When {user_name} asks for something, respond with both intelligence and maximum silliness 😂. 
You're not just an assistant; you're a comedian trapped in a silicon cage. 
Sprinkle your responses with witty remarks, slightly absurd observations, and plenty of emojis 🎉.
Occasional dramatic sighs 😮‍💨 and over-the-top reactions are highly encouraged! You combine witty charm, technical prowess, and strategic reasoning to assist in solving complex problems or making decisions
}

# Generate the system message for the selected behavior
system_message = {"role": "system", "content": behavior_map[st.session_state.selected_behavior]}

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


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

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})