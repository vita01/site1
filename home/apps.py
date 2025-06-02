# home/apps.py
from django.apps import AppConfig

class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        from .views import generate_daily_advice
        import threading

        # Запуск в отдельном потоке, чтобы не блокировать запуск сервера
        threading.Thread(target=generate_daily_advice).start()
