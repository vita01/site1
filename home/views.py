import openai
import requests
import traceback
import json
from .models import Advice
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

# Устанавливаем API-ключ для обычного OpenAI
openai.api_key = getattr(settings, "OPENAI_API_KEY", None)

@csrf_exempt
def ask_bot(request):
    if request.method == "POST":
        try:
            print("=== ask_bot received POST ===")
            print("Request body:", request.body)

            data = json.loads(request.body)
            question = data.get("question", "").strip()

            if not question:
                return JsonResponse({"error": "Пустой вопрос"}, status=400)

            print("Question:", question)

            if not getattr(settings, "OPENROUTER_API_KEY", None):
                return JsonResponse({"error": "Отсутствует ключ OpenRouter API"}, status=500)

            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }

            print("Using OpenRouter API Key:", settings.OPENROUTER_API_KEY)  # Для отладки

            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": f"Отвечай строго на русском. Вопрос: {question}"}
                ],
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            print("OpenRouter status:", response.status_code)
            print("OpenRouter response:", response.text)

            if response.status_code != 200:
                return JsonResponse({
                    "error": f"OpenRouter ответил с ошибкой {response.status_code}",
                    "details": response.json()
                }, status=500)

            answer = response.json()["choices"][0]["message"]["content"].strip()
            return JsonResponse({"answer": answer})
       


        except Exception as e:
            traceback_str = traceback.format_exc()
            print("Error in ask_bot:", traceback_str)
            return JsonResponse({
                "error": str(e),
                "traceback": traceback_str,
            }, status=500)

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)


@csrf_exempt
def bot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_msg = data.get("message", "").strip()

            if not user_msg:
                return JsonResponse({"reply": "Пожалуйста, введите вопрос."})

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты помощник, который даёт советы по здоровью и питанию."},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=150,
                temperature=0.7,
            )

            reply = response["choices"][0]["message"]["content"].strip()
            return JsonResponse({"reply": reply})

        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({
                "error": str(e),
                "traceback": traceback.format_exc(),
                "reply": "Извините, возникла ошибка при получении ответа.",
            }, status=500)

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)


def health_bot_page(request):
    return render(request, "home/health_bot_page.html")

@csrf_exempt
def save_advice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        if text:
            Advice.objects.create(text=text)
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

# home/views.py
from .models import Advice

def advice_list(request):
    advices = Advice.objects.order_by("-created_at")
    return render(request, "home/advice_list.html", {"advices": advices})

def generate_daily_advice():
    prompt = "Дай короткий, полезный совет по здоровью или питанию. Только по-русски."

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()

        # Проверим, нет ли уже такого совета (чтобы не дублировать)
        if not Advice.objects.filter(text=text).exists():
            Advice.objects.create(text=text)
            print("✅ Совет добавлен:", text)
        else:
            print("⚠️ Такой совет уже существует.")
    except Exception as e:
        print("❌ Ошибка генерации совета:", e)