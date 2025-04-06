import requests
from interviewsathi.settings import LLM_API_URL, LLM_MODEL_NAME

def deepseek_followup(prev_qas: list, resume_text: str) -> str:
    messages = [{"role": "system", "content": "You are an interview bot."}]
    messages.append({"role": "user", "content": f"Candidate resume:\n{resume_text}"})

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


def generate_final_feedback(history: list) -> str:
    messages = [{"role": "system", "content": "You're an AI interviewer. Provide a final feedback report including:\n- Communication\n- Technical Knowledge\n- Cultural Fit\nGive ratings (1-5 stars) and short descriptions."}]
    for qa in history:
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
