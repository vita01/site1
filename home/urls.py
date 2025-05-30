# home/urls.py
from django.urls import path
from .views import bot_api  # импортируем наш API для бота

urlpatterns = [
    path('bot/', bot_api, name='bot_api'),
]

