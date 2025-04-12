import chromadb
import google.generativeai as genai
import streamlit as st
from db import get_db
from GeminiEmbeddingFunction import GeminiEmbeddingFunction  
genai.configure(api_key="AIzaSyDU5ze5H_6H2TFqrbha_S0uUrloxkMf3S4")  

model = genai.GenerativeModel("models/gemini-2.0-flash")

def chat(query):
    db = get_db()

    # Example query
    
    result = db.query(query_texts=[query], n_results=5)
    [all_passages] = result["documents"]
    query_oneline = query.replace("\n", " ")

    
    prompt = f"""
You are a helpful and informative assistant for university students. 
Answer questions and explain concepts clearly and simply, using the reference passage included below to guide your response. 
Do not mention the passage or reference materials — just provide confident, natural-sounding answers.
Only rely on outside knowledge if it's absolutely necessary.
Be sure to give complete answers with useful background context, and keep your tone friendly and conversational.


    QUESTION: {query_oneline}
    """

    
    for passage in all_passages:
        passage_oneline = passage.replace("\n", " ")
        prompt += f"PASSAGE: {passage_oneline}\n"

   
    response = model.generate_content(prompt)
    return response.text
