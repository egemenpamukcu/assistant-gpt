from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import get_chatbot_response

from .models import Bot

def index(request):
    test = Bot.objects.filter()
    return render(request, 'chat.html')


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data["message"]
            response = get_chatbot_response(message)
            return JsonResponse({"message": response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except KeyError:
            return JsonResponse({"error": "Missing 'message' field in request body."}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
