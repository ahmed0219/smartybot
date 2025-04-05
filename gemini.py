import google.generativeai as genai
genai.configure(api_key="AIzaSyDU5ze5H_6H2TFqrbha_S0uUrloxkMf3S4")

model = genai.GenerativeModel("models/gemini-2.0-flash")

def chat_with_gemini(question, context):



    prompt = f"{context}\n\nAnswer qustions related to the paper only. If the question is not related to the paper, say 'I cannot answer that.'\n\nQuestion: {question}. Answer the question based on the paper content with an easy explanation that can be understood by non-experts.\n\n"
    response = model.generate_content(prompt)
    return response.text