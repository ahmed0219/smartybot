import streamlit as st
from gemini import chat
from correcteur import corrector_expert
from quiz_generator import generate_quiz
from PyPDF2 import PdfReader
import json

st.set_page_config(page_title="PaperTutor", layout="centered")

# === SESSION STATE INIT ===
if "text" not in st.session_state:
    st.session_state.text = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("📄 Streamlit PaperTutor – Learn, Chat & Quiz")

# === ASK QUESTIONS ===
st.subheader("🤖 Ask something about the paper")
user_input = st.text_input("Your question:")
if user_input:
    response = chat(user_input)
    st.markdown(f"**Gemini:** {response}")

# === GENERATE QUIZ BUTTON ===
if st.button("🧠 Generate Quiz"):
    st.session_state.quiz = generate_quiz()
    st.session_state.answers = {}  # Reset answers
    st.success("🧠 New quiz generated!")

# === DISPLAY QUIZ ===
if st.session_state.quiz:
    st.subheader("📝 Quiz Time!")

    for i, q in enumerate(st.session_state.quiz):
        st.subheader(f"Question {i+1}: {q['question']}")

        if q["type"] == "mcq":
            selected = st.radio(
                "Choose an answer:",
                q["options"],
                key=f"question_{i}"
            )
        elif q["type"] == "true_false":
            selected = st.radio(
                "True or False?",
                ["True", "False"],
                key=f"question_{i}"
            )
        else:
            selected = st.text_input("Your answer:", key=f"question_{i}")

        st.session_state.answers[f"q{i}"] = selected

if st.session_state.quiz and st.button("✅ Submit Quiz"):
    total = len(st.session_state.quiz)
    correct = 0
    feedback = []

    for i, q in enumerate(st.session_state.quiz):
        user_answer = st.session_state.answers.get(f"q{i}", "").strip()
        correct_answer = q["answer"]

        result = corrector_expert(user_answer, correct_answer)
        print(result)
        is_correct = result["correct"]
        if is_correct:
            correct += 1

        feedback.append(result)

    st.session_state.score = correct

    st.subheader(f"🎯 Your Score: {correct}/{total}")
    
    for i, message in enumerate(feedback):
        st.write(f"**Question {i+1} feedback:**")
        st.write(message.get("feedback", "No feedback provided."))
