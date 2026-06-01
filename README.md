AI Study Assistant

Overview

AI Study Assistant is a smart learning platform designed to simplify complex topics using Artificial Intelligence. The system leverages the Groq API with the LLaMA 3.1 model to provide instant explanations, generate key concepts, create visual mindmaps, analyze study materials, and recommend educational resources.
The platform helps students learn faster by combining text-based explanations, visual learning, document analysis, and AI-powered assistance in a single interface.

# Features:

- AI-powered topic explanations
- Interactive chatbot using LLaMA 3.1
- Automated key-point extraction
- Dynamic mindmap generation
- Educational video recommendations
- PDF document analysis
- Image text extraction using OCR
- User authentication and registration
- Chat history storage
- Voice input support

# Technologies Used:
# Backend:

- Python
- Django
- Groq API
- SQLite

# Frontend:

- HTML5
- CSS3
- JavaScript

# Libraries:

- requests
- PyPDF2
- pytesseract
- Pillow
- Mermaid.js

# Project Structure:

```text
ai-study-assistant/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── aichatbot/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── chatbot/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
├── static/
└── README.md
```

# How It Works:

1. User enters a topic or question.
2. Django backend receives the request.
3. Request is sent to Groq API.
4. LLaMA 3.1 processes the query.
5. AI-generated response is returned.
6. Results are displayed through the web interface.

# Core Functionalities:

# AI Chatbot: Provides conversational responses and academic guidance using Large Language Models.

# Study Material Analysis: Extracts information from uploaded PDFs and images.

# Visual Mindmaps: Generates flowcharts and visual learning structures using Mermaid.js.

# Educational Resources: Recommends learning materials and educational content related to the searched topic.

# Voice Input: Allows users to interact using speech recognition.

# Database Design:
# ChatMessage stores:

- User information
- User questions
- AI responses
- Timestamps

# Installation:
Clone the repository:

```bash
git clone https://github.com/Kusuma-Ramesh/ai-study-assistant.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

# Future Enhancements:

- AI-generated quizzes
- Personalized learning paths
- Collaborative study rooms
- PDF export functionality
- Advanced analytics dashboard
- Multi-language support

# Learning Outcomes:

- Django Web Development
- API Integration
- Database Management
- Authentication Systems
- OCR Processing
- AI Application Development
- Full Stack Development

# Author:

Kusuma R

Department of Computer Science and Engineering

B.N.M Institute of Technology
