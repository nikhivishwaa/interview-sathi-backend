from channels.generic.websocket import AsyncWebsocketConsumer
import json
from interview.models import InterviewSession, InterviewHistory, InterviewQuestion, Resume
from interview.utils.chains import model_followup, model_feedback
# from interview.utils.llm import model_followup, model_feedback
from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.utils import timezone

class ResumeCache:
    """
    This class is used to manage the candidate's resume.
    It stores the resume in a cache with a session ID as the key.
    """
    @staticmethod
    async def get(session: InterviewSession)->str:
        key = f"user_resume_{session.id}"
        data = cache.get(key)
        # Check if the resume is already cached
        if not data:
            # fetch from DB and store in cache
            data = await sync_to_async(lambda: session.resume.parsed_text)()
            cache.set(key, data, timeout=3600)  # 1 hour cache
        return data
    
    @staticmethod
    def delete(session_id:int)->None:
        key = f"user_resume_{session_id}"
        cache.delete(key)

class IntroCache:
    """
    This class is used to manage the candidate's introduction.
    It stores the introduction in a cache with a session ID as the key.
    """

    @staticmethod
    def get(session_id:int)->str:
        key = f"user_intro_{session_id}"
        data = cache.get(key)
        return f"<Candidate Introduction>{data}</Candidate Introduction>"

    @staticmethod
    def set(session_id:int, intro:str)->None:
        key = f"user_intro_{session_id}"
        cache.set(key, intro, timeout=3600)

    @staticmethod
    def delete(session_id:int)->None:
        key = f"user_intro_{session_id}"
        cache.delete(key)


class InterviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.channel_layer:
            await self.log("❌ Channel layer is not configured!")
            
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f"interview_{self.session_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await sync_to_async(self.mark_session_active)()

        # Custom intro question
        intro_question = "Welcome! Let's start with a quick introduction. Can you tell me about your background and experience?"
        await self.send(text_data=json.dumps({
            'question_id': "intro",  # ← special marker
            'question': intro_question
        }))

    def mark_session_active(self):
        session = InterviewSession.objects.get(id=self.session_id)
        session.is_active = True
        session.started_at = timezone.now()
        session.save()

    def get_first_question(self):
        session = InterviewSession.objects.get(id=self.session_id)
        return InterviewQuestion.objects.filter(
            domain=session.role,
            coming_from='pdf'
        ).order_by('?').first()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await sync_to_async(self.mark_session_inactive)()

    def compute_weighted_score(self, raw):
        return round(
            raw.get("technical",0) * 0.4 +
            raw.get("communication",0) * 0.3 +
            raw.get("relevance",0) * 0.2 +
            raw.get("grammar",0) * 0.1
        )

    def mark_session_inactive(self):
        session = InterviewSession.objects.get(id=self.session_id)
        session.ended_at = timezone.now()
        session.status = 'completed'
        session.is_active = False
        session.save()

    async def log(*args):
        await sync_to_async(print)(*args)

    async def _finalize_session(self):
        try:
            await sync_to_async(self.mark_session_inactive)()
            session = await sync_to_async(InterviewSession.objects.get)(id=self.session_id)
            await self.log("level 1")
            
            # Fetch history for feedback generation
            history = await sync_to_async(
                lambda: list(InterviewHistory.objects.filter(session=session)
                            .values("question__question_text", "answer"))
            )()
            qas = [{"question": h["question__question_text"], "answer": h["answer"]} for h in history]

            resume_text = await ResumeCache.get(session)
            
            await self.log("level 1")
            introduction = IntroCache.get(session.id)
            
            await self.log("level 2")
            feedback = await sync_to_async(model_feedback)(qas, resume_text, introduction, session.job_desc)
            await self.log("level 3")
            feedback["overall_score"] = await sync_to_async(self.compute_weighted_score)(feedback["scores"])
            session.metadata['feedback'] = feedback
            await session.asave()
            await self.log("level 4")
            # clear the cache
            ResumeCache.delete(session.id)
            IntroCache.delete(session.id)
            await self.log("level 5")

            # Store or cache feedback if needed
            cache.set(f"feedback_{session.id}", feedback, timeout=3600)
        
        except Exception as e:
            await self.log("error")
            await self.log(e)

    async def receive(self, text_data):
        # try:
        data = json.loads(text_data)

        
        await self.log("💬 Received WebSocket data:", data)  # ✅ Add this

        if data.get("type") == "end_interview":
            await self.log("Ending interview...")
            await self._finalize_session()
            await self.send(text_data=json.dumps({
                "type": "interview_ended",
                "message": "Interview ended. Feedback generated.",
                "redirect": f"/feedback/{self.session_id}/"
            }))
            return

        session = await sync_to_async(InterviewSession.objects.get)(id=self.session_id)
        if data.get('question_id')=='intro':
            IntroCache.set(session_id=session, intro=data.get('answer'))

        else:
            question_id = data['question_id']
            answer = data['answer']

            question = await sync_to_async(InterviewQuestion.objects.get)(id=question_id)

            await sync_to_async(InterviewHistory.objects.create)(
                session=session,
                question=question,
                answer=answer
            )

        resume_text = await ResumeCache.get(session)
        introduction = IntroCache.get(session.id)

        history = await sync_to_async(
            lambda: list(
                InterviewHistory.objects.filter(session=session)
                .values("question__question_text", "answer")
            )
        )()
        qas = [{"question": h["question__question_text"], "answer": h["answer"]} for h in history]

        followup_text = await sync_to_async(model_followup)(qas, resume_text, introduction, session.job_desc)
        followup_text = followup_text.lstrip('Q:')

        
        await self.log("🧠model follow-up:", followup_text)

        # Save to InterviewQuestion
        followup_q = await sync_to_async(InterviewQuestion.objects.create)(
            domain=session.role,
            question_text=followup_text,
            coming_from="model",
            source=None
        )

        await self.send(text_data=json.dumps({
            'question_id': followup_q.id,
            'question': followup_text
        })) 
        # except Exception as e:
        #   await self.log("error",e)
