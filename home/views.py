import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def bot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        # Здесь должна быть логика обращения к боту (пока эхо)
        reply = f"Вы спросили: {user_message}"

        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid method"}, status=405)
