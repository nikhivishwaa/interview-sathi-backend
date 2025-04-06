from django.db.models.signals import post_save
from django.dispatch import receiver
from interview.models import QuestionPDF, InterviewQuestion
import fitz

@receiver(post_save, sender=QuestionPDF)
def extract_questions_from_pdf(sender, instance, created, **kwargs):
    if not created:
        return
    pdf_path = instance.pdf_file.path
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    questions = [q.strip() for q in text.split('\n') if '?' in q and len(q.strip()) > 10]

    for q in questions:
        InterviewQuestion.objects.create(
            domain=instance.domain,
            question_text=q,
            source=instance,
        )
