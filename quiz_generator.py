import random
import re
import json
import streamlit as st
from gemini import model
from db import get_db  

def generate_quiz() -> list[dict]:
    db = get_db()
    num_questions = 5
    max_chunks = 50

    all_docs = db.peek()
    documents = all_docs["documents"]
    sampled_chunks = random.sample(documents, min(len(documents), max_chunks))
    context = "\n\n".join(sampled_chunks)

    prompt = f"""
You are a helpful quiz generator for students.

Using the following study content, generate {num_questions} quiz questions. Vary the format (multiple choice, true/false, and short answer).

Please return the questions as a JSON list. Each question should be an object with:
- 'question': The question text
- 'type': 'mcq', 'true_false', or 'short'
- 'options': (optional) list of options for MCQs
- 'answer': The correct answer

Study content:
\"\"\"
{context}
\"\"\"
"""

    response = model.generate_content(prompt).text
    print("Response from Gemini:", response)

    cleaned = re.sub(r"```(?:json)?", "", response).replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)

        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict) and "questions" in parsed:
            return parsed["questions"]
        else:
            st.error("Unexpected response format.")
            return []

    except json.JSONDecodeError as e:
        if st._is_running_with_streamlit:
            st.error(f"JSON parsing failed: {e}")
            st.text_area("Model Output (for debugging):", response, height=300)
        else:
            print(f"[ERROR] JSON parsing failed: {e}")
            print(response)
        return []
