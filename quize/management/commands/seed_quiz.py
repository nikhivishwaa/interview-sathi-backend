# quize/management/commands/seed_quiz.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quize.models import QuizCategory, Quiz, Question, Option
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed quiz app with meaningful quiz data including solutions"

    def handle(self, *args, **kwargs):
        # Clear previous data
        Option.objects.all().delete()
        Question.objects.all().delete()
        Quiz.objects.all().delete()
        QuizCategory.objects.all().delete()

        # Realistic categories
        categories = [
            {"name": "Frontend", "description": "Frontend development related quizzes"},
            {"name": "Backend", "description": "Backend development and databases"},
            {"name": "Fullstack", "description": "Fullstack development quizzes"},
        ]

        # Sample real questions per category with solution and description
        frontend_questions = [
            {
                "text": "What is the virtual DOM in React?",
                "options": ["A copy of the real DOM", "A database", "CSS framework", "JS runtime"],
                "correct": 0,
                "solution": "Virtual DOM is a lightweight copy of the real DOM that React uses to optimize rendering.",
                "description": "Understand how React optimizes UI rendering using virtual DOM."
            },
            {
                "text": "What is a closure in JavaScript?",
                "options": ["Function with preserved scope", "HTML element", "CSS property", "JS object"],
                "correct": 0,
                "solution": "A closure is a function that has access to its outer function's scope even after the outer function has returned.",
                "description": "Closures allow private variables and function factories."
            },
            {
                "text": "Which HTML tag is used for links?",
                "options": ["<a>", "<div>", "<span>", "<p>"],
                "correct": 0,
                "solution": "<a> tag defines a hyperlink in HTML.",
                "description": "Basic HTML knowledge for anchor tags."
            },
            {
                "text": "Which CSS property changes text color?",
                "options": ["color", "background", "font-size", "border"],
                "correct": 0,
                "solution": "The 'color' property in CSS sets the text color.",
                "description": "CSS styling basics."
            },
            {
                "text": "How do you write a comment in JavaScript?",
                "options": ["// comment", "/* comment */", "# comment", "<!-- comment -->"],
                "correct": 0,
                "solution": "Single line comments in JS use // and multi-line comments use /* */.",
                "description": "JS syntax for commenting."
            },
        ]

        backend_questions = [
            {
                "text": "What is Django?",
                "options": ["Python web framework", "Database", "CSS library", "JS framework"],
                "correct": 0,
                "solution": "Django is a high-level Python web framework that encourages rapid development and clean design.",
                "description": "Backend framework knowledge."
            },
            {
                "text": "What is a REST API?",
                "options": ["Web service", "CSS rule", "Database type", "JS function"],
                "correct": 0,
                "solution": "REST API is an architectural style for designing networked applications using HTTP requests.",
                "description": "Understand REST principles."
            },
            {
                "text": "What is ORM in Django?",
                "options": ["Object Relational Mapping", "Open Resource Model", "Online React Module", "Other"],
                "correct": 0,
                "solution": "ORM allows interaction with the database using Python objects instead of raw SQL.",
                "description": "Django ORM maps models to database tables."
            },
            {
                "text": "Which database is NoSQL?",
                "options": ["MongoDB", "PostgreSQL", "MySQL", "SQLite"],
                "correct": 0,
                "solution": "MongoDB is a NoSQL database which stores data in flexible JSON-like documents.",
                "description": "Database classification."
            },
            {
                "text": "What is middleware in Django?",
                "options": ["Hooks for request/response", "CSS library", "Database module", "JS function"],
                "correct": 0,
                "solution": "Middleware is a framework of hooks into Django's request/response processing.",
                "description": "Understanding Django request lifecycle."
            },
        ]

        fullstack_questions = frontend_questions + backend_questions  # combine for fullstack

        # Seed categories, quizzes, questions, and options
        for cat in categories:
            category = QuizCategory.objects.create(
                name=cat["name"], 
                description=cat["description"]
            )

            # 3 quizzes per category
            for qz_num in range(1, 4):
                quiz = Quiz.objects.create(
                    category=category,
                    title=f"{category.name} Quiz {qz_num}",
                    description=f"This is a {category.name} quiz number {qz_num}",
                    duration_minutes=random.choice([5, 10, 15])
                )

                # 20 questions per quiz (repeat questions if needed)
                questions_pool = (
                    fullstack_questions if category.name == "Fullstack"
                    else (frontend_questions if category.name == "Frontend" else backend_questions)
                )
                for i in range(20):
                    qdata = questions_pool[i % len(questions_pool)]
                    question = Question.objects.create(
                        quiz=quiz,
                        text=qdata["text"],
                        marks=1,
                        solution=qdata.get("solution", ""),
                        description=qdata.get("description", "")
                    )

                    for idx, opt_text in enumerate(qdata["options"]):
                        Option.objects.create(
                            question=question,
                            text=opt_text,
                            is_correct=(idx == qdata["correct"])
                        )

        self.stdout.write(self.style.SUCCESS("Realistic dummy quiz data with solutions created successfully!"))
