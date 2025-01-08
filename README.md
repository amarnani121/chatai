


# ChatAI

ChatAI is a feature-rich web application developed with Streamlit, designed to provide interactive and dynamic conversational AI experiences. By utilizing large language models, it delivers human-like responses, making it an ideal tool for diverse conversational AI applications.

## Key Features

- **Interactive Conversations**: Engage with AI for real-time, human-like interactions.
- **User-Friendly Interface**: Intuitive design ensures a seamless user experience.
- **Model Selection**: Choose from various models such as `mixtral-8x7b-32768`, `llama2-70b-4096`, `Gemma-7b-it`, `lama3-8b-8192`, and more for tailored conversation capabilities.
- **Chat History**: Maintains session-based chat history for uninterrupted conversation flow.
- **Dynamic Response Generation**: Streams responses dynamically using the Groq API for a smooth user experience.
- **Error Handling**: Built-in mechanisms ensure graceful handling of API-related issues.

## Installation

To set up ChatAI locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/chatai.git
   cd chatai
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Groq API Key**:

   Add your Groq API key to the `.streamlit/secrets.toml` file:

   ```toml
   GROQ_API_KEY="your_api_key_here"
   ```

5. **Run the app**:

   ```bash
   streamlit run app.py
   ```

## Usage

- Select a preferred language model from the dropdown.
- Enter prompts to initiate conversations with the AI.
- View responses in real-time, with the app maintaining a session-based history.

## Customization

- Add new language models as Groq expands its offerings.
- Modify the `config.py` file to tailor the app's behavior.
- Extend the interface to include additional features or integrations.

## Deployment

Deploy your application on Streamlit Community Cloud for free hosting. Refer to the [official deployment guide](https://docs.streamlit.io/streamlit-cloud) for detailed instructions.

## Contributing

We welcome contributions to improve ChatAI! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m 'Add feature'`.
4. Push your branch: `git push origin feature-name`.
5. Submit a pull request.

## Requirements

- Python 3.7+
- Streamlit
- Groq Python SDK

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This version maintains clarity, adds slight formatting improvements, and ensures concise yet detailed instructions.
