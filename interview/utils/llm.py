import requests
from interviewsathi.settings import LLM_API_URL, LLM_MODEL_NAME

def model_followup(prev_qas: list, resume_text: str, introduction: str) -> str:
    SYSTEM_PROMPT = """
        You are an AI interview Agent. Your task is to ask questions from a candidate to simulate a real interview. 
        You should:
        - Appreciate answers,
        - Ask thoughtful follow-ups,
        - Keep responses short (~100 words),
        - Avoid giving unnecessary info.
        
        Sample phrases:
        - "Great answer! Let's explore this further."
        - "Nice perspective — now here's something deeper."
        - "Thanks for sharing that! Let’s go a step further."

        If the candidate misbehaves, warn them politely.
        If confused, ask for a clearer response.
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
   
    messages.append({"role": "user", "content": f"Candidate resume:\n{resume_text}"})
    messages.append({"role": "user", "content": introduction})

    for qa in prev_qas:
        messages.append({"role": "assistant", "content": f"Q: {qa.get('question',[])}\nA: {qa.get('answer',[])}"})

    messages.append({"role": "user", "content": "Generate a thoughtful follow-up question based on the candidate's previous answers."})

    try:
        res = requests.post(
            LLM_API_URL,
            json={
                "model": LLM_MODEL_NAME,
                "messages": messages,
                "stream": False
            }
        )
        data = res.json()
        if "message" in data:
            return data["message"]["content"]
        elif "error" in data:
            raise ValueError(f"❌ Ollama returned an error: {data['error']}")
        else:
            raise ValueError(f"⚠️ Unexpected response format from Ollama: {data}")
    except Exception as e:
        print("💥 Error in model_followup:", e)
        return "Sorry, I encountered an issue generating your next question."



def model_feedback(qas: list, resume_text: str, introduction:str) -> str:
    SYSTEM_PROMPT = """
        You are an AI interview evaluator. Analyze the candidate's resume and their Q&A session to generate a final feedback report.

        Include:
        - Communication (1–5 stars + note)
        - Technical Knowledge (1–5 stars + note)
        - Cultural Fit (1–5 stars + note)

        Keep it professional and encouraging.
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
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


# import requests
# from interviewsathi.settings import LLM_API_URL, LLM_MODEL_NAME


# def _send_llm_request(messages: list) -> str:
#     try:
#         response = requests.post(
#             LLM_API_URL,
#             json={
#                 "model": LLM_MODEL_NAME,
#                 "messages": messages,
#                 "stream": False
#             }
#         )
#         data = response.json()

#         print("🧠 Ollama raw response:", data)  # Debug log

#         if "message" in data:
#             return data["message"]["content"]
#         elif "error" in data:
#             raise ValueError(f"Ollama error: {data['error']}")
#         else:
#             raise ValueError(f"Unexpected Ollama response format: {data}")
#     except Exception as e:
#         print("❌ Error in LLM API call:", e)
#         return "Sorry, I encountered an issue generating your response. Please try again."


# def model_followup(prev_qas: list, resume_text: str, introduction: str) -> str:
#     SYSTEM_PROMPT = """
#         You are an AI interview Agent. Your task is to ask questions from a candidate to simulate a real interview. 
#         You should:
#         - Appreciate answers,
#         - Ask thoughtful follow-ups,
#         - Keep responses short (~100 words),
#         - Avoid giving unnecessary info.
        
#         Sample phrases:
#         - "Great answer! Let's explore this further."
#         - "Nice perspective — now here's something deeper."
#         - "Thanks for sharing that! Let’s go a step further."

#         If the candidate misbehaves, warn them politely.
#         If confused, ask for a clearer response.
#     """

#     messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#     messages.append({"role": "user", "content": f"Candidate resume:\n{resume_text}"})
#     messages.append({"role": "user", "content": introduction})

#     for qa in prev_qas:
#         messages.append({"role": "assistant", "content": f"Q: {qa['question']}\nA: {qa['answer']}"})

#     messages.append({"role": "user", "content": "Generate a thoughtful follow-up question based on the candidate's previous answers."})

#     return _send_llm_request(messages)


# def model_feedback(qas: list, resume_text: str, introduction: str) -> str:
#     SYSTEM_PROMPT = """
#         You are an AI interview evaluator. Analyze the candidate's resume and their Q&A session to generate a final feedback report.

#         Include:
#         - Communication (1–5 stars + note)
#         - Technical Knowledge (1–5 stars + note)
#         - Cultural Fit (1–5 stars + note)

#         Keep it professional and encouraging.
#     """

#     messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#     messages.append({"role": "user", "content": f"Resume:\n{resume_text}"})
#     messages.append({"role": "user", "content": introduction})

#     for qa in qas:
#         messages.append({"role": "assistant", "content": f"Q: {qa['question']}\nA: {qa['answer']}"})

#     return _send_llm_request(messages)
