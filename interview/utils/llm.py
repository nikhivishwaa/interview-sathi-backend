import requests
from interviewsathi.settings import LLM_API_URL, LLM_MODEL_NAME

def model_followup(prev_qas: list, resume_text: str, introduction:str) -> str:
    messages = [{"role": "system", "content": "You are an interview bot."}]
    messages.append({"role": "user", "content": f"Candidate resume:\n{resume_text}"})
    messages.append({"role": "user", "content": introduction})

    for qa in prev_qas:
        messages.append({"role": "assistant", "content": f"Q: {qa['question']}\nA: {qa['answer']}"})

    messages.append({"role": "user", "content": "Generate a thoughtful follow-up question based on the candidate's previous answers."})

    res = requests.post(
        LLM_API_URL,  # Ollama endpoint
        json={
            "model": LLM_MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )
    return res.json()['message']['content']


def model_feedback(qas: list, resume_text: str, introduction:str) -> str:
    messages = [{"role": "system", "content": "You are an AI interview evaluator. Analyze the following conversation and Provide a final feedback report including:\n- Communication\n- Technical Knowledge\n- Cultural Fit\nGive ratings (1-5 stars) and short descriptions."}]
    messages.append({"role": "user", "content": f"Resume:\n{resume_text}"})
    messages.append({"role": "user", "content": introduction})

    for qa in qas:
        messages.append({"role": "assistant", "content": f"Q: {qa['question']}\nA: {qa['answer']}"})

    res = requests.post(
        LLM_API_URL,  # Ollama endpoint
        json={
            "model": LLM_MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )
    return res.json()['message']['content']

