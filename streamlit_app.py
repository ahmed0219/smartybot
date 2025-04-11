import streamlit as st

from gemini import chat
from correcteur import corrector_expert
from quiz_generator import generate_quiz
from PyPDF2 import PdfReader
import json

# Streamlit Page Setup
st.set_page_config(page_title="PaperTutor", layout="centered")

# Initialize session state variables if they are not already initialized
if "text" not in st.session_state:
    st.session_state.text = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:  # Initialize answers if not already done
    st.session_state.answers = {}

st.title("📄 Streamlit PaperTutor – Learn, Chat & Quiz")




st.subheader("🤖 Ask something about the paper")
user_input = st.text_input("Your question:")
if user_input:
        response = chat(user_input)
        st.markdown(f"**Gemini:** {response}")

