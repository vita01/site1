from django.contrib import admin
from django.urls import path, include
from wagtail import urls as wagtail_urls

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', include('wagtail.admin.urls')),
    path('documents/', include('wagtail.documents.urls')),

    # Кастомные маршруты
    path("health-bot-page/", views.health_bot_page, name="health_bot_page"),
    path("api/ask_bot/", views.ask_bot, name="ask_bot"),
    path("api/save_advice/", views.save_advice, name="save_advice"),
    path("advice-list/", views.advice_list, name="advice_list"),

    # В конце — wagtail (обрабатывает всё остальное)
    path('', include(wagtail_urls)),
]
