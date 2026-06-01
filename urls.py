"""
Project-level URL configuration.
Routes requests to the chatbot app and Django's auth system.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django built-in auth URLs (login, logout, password change, etc.)
    path('', include('django.contrib.auth.urls')),

    # Our chatbot app's URLs
    path('', include('chatbot.urls')),
]
