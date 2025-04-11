import chromadb
import google.generativeai as genai
import streamlit as st
from db import get_db

genai.configure(api_key="")  

model = genai.GenerativeModel("models/gemini-2.0-flash")

def chat(query):
    # Get the database instance
    db = get_db()
   
   


    result = db.query(query_texts=[query], n_results=1)  
    documents = result["documents"]  
    query_oneline = query.replace("\n", " ")

    
    prompt = f"""
    You are a helpful and informative bot for university students that answers questions and explains concepts using the text from the reference passage included below.
    You may use other knowledge only if it is absolutely necessary.
    Be sure to respond with a complete sentence, including relevant background information, and explain complicated concepts in simple terms. Maintain a friendly and conversational tone.

    QUESTION: {query_oneline}
    """

    
    for passage in documents:
        passage_oneline = passage.replace("\n", " ")
        prompt += f"PASSAGE: {passage_oneline}\n"

   
    response = model.generate_content(prompt)
    return response.text
