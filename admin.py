"""
Register models with Django Admin panel.
"""

from django.contrib import admin
from .models import ChatMessage

# Register ChatMessage so you can view chat history in the admin panel
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'created_at')
    list_filter = ('user',)
    search_fields = ('user_message', 'bot_response')
