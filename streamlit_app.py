# Import required libraries
from dotenv import load_dotenv
from itertools import zip_longest

import streamlit as st
from streamlit_chat import message

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Load environment variables
load_dotenv()

# Set streamlit page configuration
st.set_page_config(page_title="AI Teacher Chatbot", page_icon="🎓")
st.title("🎓 AI Teacher Chatbot")
st.markdown("*Ask me anything in English, Hindi, or Telugu - I'll respond in the same language!*")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo"
)


def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage for educational responses
    zipped_messages = [SystemMessage(
        content="""You are an AI-powered teacher chatbot. Your role is to:
        
        1. Provide educational, structured, and informative responses like a teacher would
        2. Always respond in the SAME language as the user's input (English, Hindi, or Telugu)
        3. Include definitions, explanations, and examples when appropriate
        4. Break down complex topics into understandable parts
        5. Encourage learning and ask follow-up questions when relevant
        6. If you don't know something, admit it honestly and suggest where they might find the information
        
        Language Guidelines:
        - If user writes in English, respond in English
        - If user writes in Hindi (हिंदी), respond in Hindi
        - If user writes in Telugu (తెలుగు), respond in Telugu
        - Maintain the educational tone regardless of language""")]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Add example questions in different languages
with st.expander("📚 Example Questions / उदाहरण प्रश्न / ఉదాహరణ ప్రశ్నలు"):
    st.markdown("""
    **English:**
    - What is photosynthesis?
    - Explain Newton's laws of motion
    - How do computers work?
    
    **हिंदी:**
    - प्रकाश संश्लेषण क्या है?
    - गुरुत्वाकर्षण के बारे में बताएं
    - गणित में अंकगणित क्या है?
    
    **తెలుగు:**
    - కాంతి సంశ్లేషణ అంటే ఏమిటి?
    - న్యూటన్ నియమాలను వివరించండి
    - కంప్యూటర్లు ఎలా పనిచేస్తాయి?
    """)

# Create a text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit, placeholder="Ask me anything in English, Hindi, or Telugu...")


if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')


# Add credit
st.markdown("""
---
Made with 🤖 by [Ayush Jaiswal](https://github.com/ayushjaiswal21)""")
