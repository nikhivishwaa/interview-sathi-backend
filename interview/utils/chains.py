from interviewsathi.settings import LLM_MODEL_NAME
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME)
parser = StrOutputParser()
json = JsonOutputParser()

def model_followup(prev_qas: list, resume_text: str, introduction: str, job_desc:str) -> str:
    SYSTEM_PROMPT = """
        You are an AI interview agent.

        Your task is to ask **relevant follow-up questions** to simulate a realistic interview based on:
        - The candidate's resume
        - Their introduction
        - The job description

        💡 You MUST:
        - Stick strictly to topics relevant to the job role (e.g., Frontend = JavaScript, UI, React, etc.)
        - Use previous Q&A history to go deeper in a focused area
        - Avoid unrelated topics like marketing or sales if the job is technical
        - Use clear, professional phrases that engage and encourage the candidate

        🗨️ Example opening phrases you can use:
        - "That’s an insightful response! Can you expand on..."
        - "Thanks for explaining that — now let’s dive deeper into..."
        - "Nice! I’d like to explore your understanding of..."
        - "That was well-put. Here’s a follow-up for you..."

        ✅ Output Format:
        - ONLY return a **single follow-up question** with one introductory phrase.
        - Do NOT include labels like “Q:”, “Follow-up:”, quotes, or bullets.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Candidate Resume:\n{resume}"),
        ("user", "Job Description:\n{job_desc}"),
        ("ai", "Thanks for sharing your resume!"),
        ("ai", "Great to meet you! Tell me about your background and experience?"),
        ("user", "Candidate Introduction:\n{introduction}"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "Please generate the next relevant follow-up question.")
    ])

    history_messages = [
        ("assistant", f"Q: {qa['question']}\nA: {qa['answer']}") for qa in prev_qas
    ]

    chain = prompt | model | parser
    return chain.invoke({
        "resume": resume_text,
        "introduction": introduction,
        "history": history_messages,
        "job_desc": job_desc
    })




def model_feedback(qas: list, resume_text: str, introduction: str, job_desc:str) -> str:
    SYSTEM_PROMPT = """
    You are an AI interview evaluator.

    You will receive:
    - The candidate’s resume
    - Their self-introduction
    - The job description
    - A list of interview questions and answers

    Your task is to assess the candidate’s performance and return a structured JSON response.

    ---------------------------------------------
    📏 **Important Scoring Rules**:

    ## Evaluate based on the following 4 criteria:
        1. **Technical** - understanding of domain-specific knowledge (40%)
        2. **Communication** - clarity, structure, vocabulary (30%)
        3. **Answer Relevance** - contextual fit of answers (20%)
        4. **Grammar Accuracy** - grammar, sentence quality (10%)

    🔍 Special Scenarios:
    - If 0-1 answers are given → All scores should be very low (0-5) and justification must state "insufficient data".
    - If user haven't responded any question or dont have introduction,  so no doubt all the scores will be zero".
    - If answers are out-of-context or irrelevant → Penalize heavily in Technical & Relevance.

    
    ## Provide:
        - 3-5 strengths
        - 3-5 improvements
        - 1-paragraph detailed feedback

    ⚠️ Do NOT exceed format.
    Return ONLY the following Valid JSON:

    🎯 Output Required:
    Return the following JSON format:
    ```
    {{
    "scores": {{
        "technical": <int>,         // 0-100
        "communication": <int>,     // 0-100
        "relevance": <int>,         // 0-100
        "grammar": <int>            // 0-100
    }},
    "strengths": ["...", "...", "..."],
    "improvements": ["...", "...", "..."],
    "detailed_feedback": "<string: 3-6 lines detailed feedback>",
    "behavioral_feedback": "<string: 2-3 lines on behavioral feedback and assessing candidate's cultural fitness>",
    }}
    ```
    """

    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Candidate resume:\n{resume}"), 
        ("user", "Candidate job description:\n{job_desc}"),
        ("ai", "Great to meet you! Tell me about your background and experience?"),
        ("user", "Candidate intro:\n{introduction}"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "Total number of questions answered: {qa_count}\nPlease generate the final interview feedback based on all this.")
    ])

    history_messages = [
        ("assistant", f"Q: {qa['question']}\nA: {qa['answer']}") for qa in qas
    ]

    chain = prompt | model | json

    result = chain.invoke({
        "resume": resume_text,
        "introduction": introduction, 
        "history": history_messages,
        "job_desc": job_desc,
        "qa_count": len(qas)
    })


    print("Feedback result:", result)
    return result
