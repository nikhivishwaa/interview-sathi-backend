# 🎤 Interview Sathi

**Interview Sathi** is an AI-driven mock interview platform designed to simulate real-time technical interviews with dynamic question generation, personalized follow-ups, resume analysis, and instant feedback. It empowers candidates to practice effectively and improve their communication, technical knowledge, and cultural fit.

---

## 🚀 Features

* 🧠 **AI-Powered Interviews** using **Gemini**
* 📄 **Resume Upload & Analysis** for tailored interview questions
* 📚 **Role-Based Question Banks** (Frontend / Backend)
* 🧾 **PDF Upload & Question Extraction** via Django Admin
* 📢 **Speech-to-Text** and 🗣️ **Text-to-Speech** for voice-enabled interaction
* 🧵 **Multi-turn Questioning** with intelligent follow-ups
* 🔍 **Real-time Feedback** and **Final Ratings**
* 🗓️ **Interview Scheduling** with session history
* 🧠 **RAG-based Question Generation** (Frontend + Backend)
* 💾 **Interview History Tracking** with answer-question linkage

---

## 🛠️ Tech Stack

### Frontend

* **Tailwind CSS**
* **React + Context API**
* **Axios** for API calls
* **Chrome Web Speech API** (TTS + STT)

### Backend

* **Django 5.1**
* **Django Channels** (Real-time communication)
* **PostgreSQL**
* **LangChain + Gemini**
* **Redis** for performance

---

## ⚙️ Setup Instructions

`requirements:`
- `Docker`
- `Git Cli`
- `RAM 8GB or Above`
- `Python 3.12`
- `Node.js LTS 18 or above`
  
### 1. Clone Repository

```bash
git clone https://github.com/nikhivishwaa/interview-sathi-backend.git backend
git clone https://github.com/nikhivishwaa/interview-sathi-frontend.git frontend
cd backend
```

### 2. Backend Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigration
python manage.py migrate
python manage.py createsuperuser
```

### 3. Stop Server and Run Following Command
```bash
docker compose up
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 5. Start Backend & Frontend

* Backend: `docker compose up`
* Frontend: `npm run dev`

---

## 🙌 Contributors

* 👨‍💻 Nikhil Vishwakarma
  [GitHub](https://github.com/nikhivishwaa) | [LinkedIn](https://linkedin.com/in/nikhivishwa)

* 👨‍💻 Nikhlesh Shukla
  [GitHub](https://github.com/Nikhleshshukla123) | [LinkedIn](https://linkedin.com/in/nikhlesh-shukla-59713325a)

* 👨‍💻 Ankush Gupta Vishwakarma
  [GitHub](https://github.com/ankushgupta05) | [LinkedIn](https://linkedin.com/in/ankush-gupta-b734b025b)

* 👨‍💻 Mustafa Qasim ALi
  [GitHub](https://github.com/hussainali99a) | [LinkedIn](https://linkedin.com/in/mustafa-qasim-ali)

---
