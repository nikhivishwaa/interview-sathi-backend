FROM python:3.12-alpine

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations && python manage.py migrate

# ENTRYPOINT [ "daphne", "-b", "0.0.0.0", "-p", "8000", "interviewsathi.asgi:application"]
ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "interviewsathi.asgi:application", "--reload" ]