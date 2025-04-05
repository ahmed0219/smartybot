import re
import json
import streamlit as st
from gemini import model

def generate_quiz(text):
    prompt = f"""
    You are an AI designed to generate multiple-choice questions from research papers. 
    Your task is to create a set of 5 multiple-choice questions based on the following paper. 
    Each question should have 4 possible answers, with one correct answer.
    Format:
    {{
      "title": "Titre du Quiz",
      "type": "QCM",
      "questions": [
          {{
              "question": "Texte de la question",
              "options":["option1", "option2", "option3", "option4"], 
              "answer": "Réponse correspondante"
          }}
      ]
    }}

    Respond ONLY with this JSON format. Do not include explanations.

    Paper content:
    {text[:3000]}
    """

    response = model.generate_content(prompt).text
    print("RAW RESPONSE:\n", response)

    # Remove triple backticks and language tags like ```json
    cleaned = re.sub(r"```(?:json)?", "", response).strip("` \n")

    try:
        quiz_data = json.loads(cleaned)
        return quiz_data.get("questions", [])
    
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing failed: {e}")
        st.text_area("Model Output (for debugging):", response, height=300)
        return []
