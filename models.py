"""
Models for the chatbot app.
Stores chat history for each user.
"""

from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    """Stores each chat message sent to the AI and its response."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the logged-in user
    user_message = models.TextField()                          # What the user typed
    bot_response = models.TextField()                          # What the AI replied
    created_at = models.DateTimeField(auto_now_add=True)       # Timestamp

    def __str__(self):
        return f"{self.user.username}: {self.user_message[:50]}"

    class Meta:
        ordering = ['created_at']  # Show oldest message first
