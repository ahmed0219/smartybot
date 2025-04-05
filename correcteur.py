from gemini import model
def corrector_expert(user_answer, correct_answer, paper_text):
    prompt = f"""
    You are an AI corrector designed to compare the user's answers with the correct answers.
    Instructions:
    1. Compare the user answer with the correct answer.
    2. If the answer is correct, return "Correct!"
    3. If the answer is incorrect, return "Incorrect! and explain why according to the paper."
    User answer: {user_answer}
    Correct answer: {correct_answer}
    Paper context: {paper_text}
    """
    # Ideally, you would send this prompt to the LLM (Gemini) here and return the response.
    # For now, let's assume the AI provides a response based on the above input.
    # This can be connected with the gemini API in the real implementation.
    
    # Sample response for illustration purposes
    response = model.generate_content(prompt).text
    return response