from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI
import json
import logging

from .models import Advice

# Инициализация клиента OpenAI с OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)


def health_bot_page(request):
    return render(request, "home/health_bot_page.html")


@csrf_exempt
def ask_bot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "").strip()
            if not question:
                return JsonResponse({"error": "Вопрос не может быть пустым"}, status=400)

            # Здесь вызываешь openrouter/openai
            completion = client.chat.completions.create(
                model=settings.OPENROUTER_MODEL,
                messages=[
                    {"role": "user", "content": question},
                ],
            )
            answer_text = completion.choices[0].message.content.strip()

            if not answer_text:
                answer_text = "Совет не сгенерирован."

            return JsonResponse({"answer": answer_text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

def generate_daily_advice(request):
    if request.method == "POST":
        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "TestBot",
                },
                extra_body={},
                model=settings.OPENROUTER_MODEL,
                messages=[
                    {"role": "user", "content": "Напиши совет по здоровью для похудения."}
                ],
            )
            text = completion.choices[0].message.content.strip()
            if not text:
                text = "Совет не сгенерирован."
            return JsonResponse({"advice": text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
@csrf_exempt
def save_advice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        if text:
            Advice.objects.create(text=text)
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


def advice_list(request):
    advices = Advice.objects.order_by("-created_at")
    return render(request, "home/advice_list.html", {"advices": advices})
