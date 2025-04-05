import streamlit as st
from utils import extract_text_from_pdf
from gemini import chat_with_gemini, model
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

# Upload Paper
uploaded_file = st.file_uploader("Upload a research paper (PDF)", type=["pdf"])
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.session_state.text = text
    st.success("Paper uploaded and processed!")

# Chat with Gemini
if st.session_state.text:
    st.subheader("🤖 Ask something about the paper")
    user_input = st.text_input("Your question:")
    if user_input:
        response = chat_with_gemini(user_input, st.session_state.text)
        st.markdown(f"**Gemini:** {response}")

# Generate Quiz
# Generate Quiz
if st.session_state.text:
    if st.button("🧠 Generate Quiz", key="generate_quiz_button"):
        # Always generate a new quiz from the model
        st.session_state.quiz = generate_quiz(st.session_state.text)
        st.session_state.answers = {}  # Clear previous answers
        st.success("🧠 New quiz generated!")


# Take the Quiz
if st.session_state.quiz:
    st.subheader("📝 Quiz Time!")
    user_answers = []


    for i, q in enumerate(st.session_state.quiz):
        st.subheader(f"Question {i+1}: {q['question']}")
        selected_option = st.radio(
            f"Choose an answer:",
            q["options"],
            key=f"question_{i}"
        )
        # Store the selected answer in session_state
        st.session_state.answers[f"q{i}"] = selected_option

    # Place the submit button outside the loop with a unique key
    if st.button("✅ Submit Quiz", key="submit_quiz_button"):
        score = 0
        feedback = []

        for i, question in enumerate(st.session_state.quiz):
            user_answer = st.session_state.answers.get(f"q{i}", "")
            correct_answer = question["answer"]

            # Use your custom feedback function
            feedback_message = corrector_expert(user_answer, correct_answer, st.session_state.text)
            feedback.append(feedback_message)

            if user_answer == correct_answer:
                score += 1

        st.session_state.score += score
        st.success(f"✅ You got {score} out of {len(st.session_state.quiz)}!")
        st.info(f"🏆 Total Score: {st.session_state.score}")

        # Feedback
        st.subheader("📋 Feedback on your answers")
        for i, message in enumerate(feedback):
            st.write(f"**Question {i+1} feedback:**")
            st.write(message)
