import json
import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI CHATBOT",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))

config_data = json.load(open(f"{working_dir}/config.json"))

API_KEY = config_data["GROq_API_KEY"]

os.environ["GROq_API_KEY"] = API_KEY

client = Groq()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Q/A ChatBot")

# Display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "You are a helpful assistant that uses previous responses to generate context-aware answers."},
        *st.session_state.chat_history  # Including all previous chat history
    ]

    # Fetching the response from the LLAMA model
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    # Save the assistant's response in chat history
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
