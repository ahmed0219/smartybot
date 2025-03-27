from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=("AIzaSyDU5ze5H_6H2TFqrbha_S0uUrloxkMf3S4"))  # Ensure you use the API key securely
model = genai.GenerativeModel("gemini-1.5-pro") 
chat = model.start_chat(history=[])

if 'chat' not in st.session_state:
    st.session_state['chat'] = model.start_chat(history=[])

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'waiting_for_answer' not in st.session_state:
    st.session_state['waiting_for_answer'] = False

if 'pending_question' not in st.session_state:
    st.session_state['pending_question'] = ""


# Function to get a response while preserving context
def get_gemini_response(question):
    """Fetches a fun and educational response for kids and updates the AI's memory."""
    prompt = (
        "You are an educational chatbot for kids! "
        "Make your responses engaging, simple, and full of emojis. "
        "Encourage learning while keeping things fun. Give them funny exercises if they ask, correct their answers, "
        "help with homework, and make them feel like they're learning with a friend. "
        "You can also teach them about math, science, languages, and more! 🚀 " \
        "don't answer non-educational questions, give inappropriate content, or ask for personal information. "
        "and help with homework. Make it simple, engaging, and educational! 🎉 "
        f"Here's the latest question: {question}"
    )
    chat = st.session_state['chat']
    response = chat.send_message(prompt, stream=True)  # Stream the response to keep context alive
    return response


# Streamlit App UI Configuration
st.set_page_config(page_title="Chat with SmartyBot! 🤖✨", page_icon="🤖")
st.title("SmartyBot 🤖 - Your Funny Learning Buddy!")
st.subheader("Ask me anything fun and educational! 🎉")

st.sidebar.header("📜 Chat History")

# Function to delete individual history entries
def delete_history(index):
    del st.session_state.history[index]

# Display conversation history
for i, entry in enumerate(st.session_state.history):
    st.markdown(f"**👦 You:** {entry['input']}")
    st.markdown(f"**🤖 SmartyBot:** {entry['response']}")
    st.divider()

input = st.text_input("Type your response or ask a new question! 🤔", key="input")
submit = st.button("🎤 Send")

if submit and input:
    if st.session_state.waiting_for_answer:
        # Simple math validation for exercises
        correct_answer = eval(st.session_state.pending_question)
        if input.strip() == str(correct_answer):
            response_text = f"🎉 Correct! {st.session_state.pending_question} = {correct_answer}! You're a math genius! 🏆"
        else:
            response_text = f"Oops! Not quite! The correct answer is {correct_answer}. Try another one! 😊"
        st.session_state.waiting_for_answer = False
        st.session_state.pending_question = ""
    else:
        # Get response from Gemini AI while keeping the chat context alive
        response = get_gemini_response(input)
        response_text = ''.join([chunk.text for chunk in response])
        
        # Detect if a math exercise is given and set up a pending answer
        if "Question" in response_text and "Tell me!" in response_text:
            st.session_state.waiting_for_answer = True
            st.session_state.pending_question = response_text.split("Tell me!")[0].split("?")[-1].strip()
        
    # Update the conversation history
    st.session_state.history.append({"input": input, "response": response_text})
    st.rerun()