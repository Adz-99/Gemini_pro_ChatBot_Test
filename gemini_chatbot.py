import os

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

working_directory=os.path.dirname(os.path.abspath(__file__))

# Load environment variables
load_dotenv(override=True)

# configure streamlit page settings
st.set_page_config(page_title="Chat with Gemini Pro",
                   page_icon=":brain:", # Favicon emoji
                   layout="centered") # Layour options  

# Load API key
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY = st.secrets("GOOGLE_API_KEY")

# Setup google gemini-pro AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# function to translate role between gemini and streamlit
def translate_role_for_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# initialise chat session if not already
if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

# Display the app title
st.title("🤖 Gemini Pro - ChatBot!")   

# Display the chat history
for message in st.session_state.chat_session.history:
        with st.chat_message(name=translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Ask Gemini Pro...")

if user_prompt:
    
    # Add user's prompt to chat
    st.chat_message(name="user").markdown(user_prompt)

    # Get model's response
    response = st.session_state.chat_session.send_message(user_prompt)
    result = response.text

    # Print response to screen
    with st.chat_message(name="assistant"):
         st.markdown(result)
