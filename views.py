"""
Views for the chatbot app.
Contains all page logic + Groq AI API integration.
"""

import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .forms import SignUpForm
from .models import ChatMessage


# ------------------------------------------------
# GROQ AI API HELPER
# Free API — sign up at https://console.groq.com
# Uses llama3-8b — fast and student-friendly answers
# ------------------------------------------------
def ask_ai(user_input):
    """
    Sends a prompt to Groq API (free, no credit card).
    Uses llama3-8b-8192 model — fast and accurate.
    Returns the AI response as a plain string.
    """
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",   # Updated free model on Groq
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful student assistant. Give short, clear, beginner-friendly answers. Keep responses under 100 words."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)

        if response.status_code == 401:
            return "Invalid API key. Please check your GROQ_API_KEY in settings.py."

        if response.status_code != 200:
            # Show the real error from Groq to help debugging
            try:
                err = response.json()
                msg = err.get("error", {}).get("message", response.text)
            except Exception:
                msg = response.text
            return f"Groq API error: {msg}"

        data = response.json()
        # Groq returns OpenAI-compatible format
        text = data["choices"][0]["message"]["content"].strip()
        return text if text else "I'm not sure. Please try rephrasing your question!"

    except requests.exceptions.Timeout:
        return "The AI is taking too long to respond. Please try again."
    except Exception as e:
        return f"Connection error: {str(e)}"


def get_topic_info(topic):
    """
    Uses Groq AI to generate topic explanation, key points,
    and Mermaid.js syntax for a visual flowchart and mindmap.
    """
    # 1. Simple Explanation
    explanation = ask_ai(f"Explain '{topic}' in simple words for a student in 2-3 sentences.")

    # 2. Key Facts
    facts_raw = ask_ai(f"List 4 short key facts about '{topic}'. Write each fact on a new line starting with a dash (-).")
    facts = [f.strip("-*• ").strip() for f in facts_raw.splitlines() if f.strip()]

    # 3. Mermaid Flowchart (graph TD)
    flowchart_prompt = (
        f"Create a simple Mermaid.js flowchart (graph TD) for '{topic}'. "
        "Use 3-5 nodes. Use ONLY single-letter IDs like A, B, C. "
        "Example: A[\"Start\"] --> B[\"Step 1\"]. Return ONLY the code."
    )
    flowchart = ask_ai(flowchart_prompt)

    # 4. Mermaid Mindmap (Using stable graph LR)
    mindmap_prompt = (
        f"Create a simple Mermaid.js graph LR for '{topic}'. "
        f"Start with A[\"{topic}\"]. Branch it to 3 nodes: B, C, D. "
        "Example: A[\"Root\"] --> B[\"Leaf\"]. Return ONLY the code."
    )
    mindmap = ask_ai(mindmap_prompt)

    def clean_mermaid(code, topic):
        # Remove any leading/trailing garbage
        cleaned = code.strip().replace("```mermaid", "").replace("```", "").replace("mermaid", "").strip()
        # Find the first mention of 'graph' and start from there
        if "graph" in cleaned.lower():
            start_idx = cleaned.lower().find("graph")
            cleaned = cleaned[start_idx:]
        
        # If still not valid, return a safe fallback
        if not cleaned.lower().startswith("graph"):
            return f'graph TD\n  A["{topic}"]'
        
        return cleaned

    return {
        "explanation": explanation,
        "key_points": facts[:4],
        "flowchart": clean_mermaid(flowchart, topic),
        "mindmap": clean_mermaid(mindmap, topic)
    }


# ------------------------------------------------
# PAGE VIEWS
# ------------------------------------------------

def home(request):
    """Home page — redirect to dashboard if logged in, else to login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def signup_view(request):
    """Signup page — lets new users create an account."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard page — shown after login. Has topic search."""
    return render(request, 'dashboard.html')


@login_required
def chat_view(request):
    """Chat page — shows chat history for the logged-in user."""
    messages = ChatMessage.objects.filter(user=request.user)
    return render(request, 'chat.html', {'messages': messages})


# ------------------------------------------------
# API ENDPOINTS (called by JavaScript fetch)
# ------------------------------------------------

@login_required
@csrf_exempt
def chat_api(request):
    """
    API endpoint for the chatbot.
    Receives a message via POST JSON, calls Groq AI,
    saves the conversation, and returns the AI response.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    # Get AI response from Groq
    bot_response = ask_ai(user_message)

    # Save to database
    ChatMessage.objects.create(
        user=request.user,
        user_message=user_message,
        bot_response=bot_response
    )

    return JsonResponse({'response': bot_response})


@login_required
@csrf_exempt
def search_api(request):
    """
    API endpoint for topic search.
    Receives a topic via POST JSON and returns
    explanation, key points, and mind map.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not topic:
        return JsonResponse({'error': 'Empty topic'}, status=400)

    result = get_topic_info(topic)
    return JsonResponse(result)
