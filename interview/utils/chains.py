from interviewsathi.settings import LLM_MODEL_NAME
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME)
parser = StrOutputParser()
output_chain = model | parser

def model_followup(prev_qas: list, resume_text: str, introduction: str, job_desc:str) -> str:
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
        # you can also use your own professional phrase as well

        If the candidate misbehaves, warn them politely.
        If confused, ask for a clearer response.

        Guideline:
        - Use the job description and the candidate's resume to generate a follow-up question.
        - Use the previous Q&A to generate a follow-up question.
        - Use the mentioned skill to generate a follow-up question.
        - Use the candidate's introduction to generate a follow-up question.
        - only give the question, & respective phrase, no another information or suffix, prefix like (Q:, Q:Q:.., *,** etc).
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Candidate resume:\n{resume}"),
        ("user", "Candidate job description:\n{job_desc}"),
        ('ai', "Thanks for sharing your resume!"),
        ("ai", "Great to meet you! Tell me about your background and experience?"),
        ("user", "Candidate intro:\n{introduction}"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "Generate a thoughtful follow-up question.")
    ])

    history_messages = [
        ("assistant", f"Q: {qa['question']}\nA: {qa['answer']}") for qa in prev_qas
    ]

    chain = prompt | output_chain
    return chain.invoke({
        "resume": resume_text,
        "introduction": introduction,
        "history": history_messages,
        "job_desc": job_desc
    })


def model_feedback(qas: list, resume_text: str, introduction: str, job_desc:str) -> str:
    SYSTEM_PROMPT = """
        You are an AI interview evaluator.
        Analyze the candidate's resume, Provided Job Desciption and their Q&A session to generate a final feedback report.

        Include:
        - Communication (1–5 stars + note)
        - Technical Knowledge (1–5 stars + note)
        - Cultural Fit (1–5 stars + note)

        Keep it professional, short, honest, and encouraging.
    """

    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Candidate resume:\n{resume}"), 
        ("user", "Candidate job description:\n{job_desc}"),
        ("ai", "Great to meet you! Tell me about your background and experience?"),
        ("user", "Candidate intro:\n{introduction}"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "Please generate the final interview feedback.")
    ])

    history_messages = [
        ("assistant", f"Q: {qa['question']}\nA: {qa['answer']}") for qa in qas
    ]

    chain = prompt | output_chain

    result = chain.invoke({
        "resume": resume_text,
        "introduction": introduction, 
        "history": history_messages,
        "job_desc": job_desc
    })

    print("Feedback result:", result)
    return result
