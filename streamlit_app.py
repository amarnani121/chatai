import streamlit as st
from typing import Generator
from datetime import datetime
from groq import Groq
import json

# Streamlit Page Config
st.set_page_config(page_icon="🚀", layout="wide", page_title="Let’s Talk with Amar’s AI")

# Sidebar UI Improvements
with st.sidebar:
    st.markdown("## ⚙️ AI Settings")  # Title for sidebar

    # Model Selection
    st.markdown("### 🤖 Choose Model")
    model_option = st.selectbox(
        "Select a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"]
    )

    # Behavior Selection (Directly as a list)
    st.markdown("### 🎭 AI Personality")
    behavior_option = st.radio("Select AI behavior:", behaviors, index=behaviors.index(st.session_state.selected_behavior))

    # Update session state
    if st.session_state.selected_model != model_option:
        st.session_state.selected_model = model_option
        st.session_state.messages = []  # Reset on model change

    if st.session_state.selected_behavior != behavior_option:
        st.session_state.selected_behavior = behavior_option
        st.session_state.messages = []  # Reset on behavior change

    # Chat Export Feature
    def save_chat():
        with open("chat_history.json", "w") as f:
            json.dump(st.session_state.messages, f)

    st.button("💾 Download Chat", on_click=save_chat)

    # Clear Chat Button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# Display chat messages with time stamps
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    timestamp = datetime.now().strftime("%I:%M %p")  # Get current time

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(f"**{timestamp}** — {message['content']}")

# Typing Indicator While AI is Processing
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # AI Response Processing
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[system_message] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=models[model_option]["tokens"],
            stream=True
        )

        # Use Typing Indicator
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI is thinking... 💭"):  # Show loading animation
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e, icon="🚨")

    # Save AI response
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})