import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def bot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "").strip()

        if not user_msg:
            return JsonResponse({"reply": "Пожалуйста, введите вопрос."})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты помощник, который даёт советы по здоровью и питанию."},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = "Извините, возникла ошибка при получении ответа."

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)
