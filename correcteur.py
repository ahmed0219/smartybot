from gemini import model

def corrector_expert(user_answer, correct_answer):
    prompt = f"""
You are a grading assistant.

Compare the student's answer to the correct answer and return:
- whether the answer is correct (True/False)
- a brief explanation

Student Answer: {user_answer}
Correct Answer: {correct_answer}

Respond in this format:
{{"correct": true/false, "feedback": "explanation here"}}
"""
    response = model.generate_content(prompt).text

    import json, re
    try:
        # Extract only the JSON object using regex (more reliable than stripping backticks)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            raise ValueError("No JSON found in response.")
    except Exception as e:
        return {"correct": False, "feedback": f"Could not parse feedback. Error: {e}"}
