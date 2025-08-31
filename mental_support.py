import streamlit as st
import google.generativeai as genai
import base64
import os

# Configure Streamlit page
st.set_page_config(page_title="Mental Health Chatbot")

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load background image as base64
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background.png")

# Add background style
st.markdown(f"""
    <style>
        .main{{
            background-image:url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
    """, unsafe_allow_html=True)

# Session state for conversation history
st.session_state.setdefault('conversation_history', [])

# Create Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Function to handle conversation
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    # Prepare prompt with chat history
    conversation_prompt = "\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in st.session_state['conversation_history']
    ])

    response = model.generate_content(conversation_prompt)
    ai_response = response.text

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Function for affirmations
def generate_affirmation():
    response = model.generate_content(
        "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    )
    return response.text

# Function for meditation guide
def generate_meditation_guide():
    response = model.generate_content(
        "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    )
    return response.text

# UI Title
st.title("Mental Health Support Agent")

# Display chat history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# User input field
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Two-column buttons for extra features
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
