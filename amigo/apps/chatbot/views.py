from django.shortcuts import render
import json
from django.http import JsonResponse
from .handlers.chat_handler import get_chatbot_response
from django.contrib.auth.decorators import login_required

def index(request):
    user = request.user
    if f'messages{user}' in request.session:
        del request.session[f'messages{user}']

    if request.session.session_key is None:
        request.session.save()

    name = request.GET.get('name')

    if not name:
        return JsonResponse({"error": "Missing 'name' parameter."}, status=400)
    
    context = {'name': name}
    return render(request, 'chat.html', context)


@login_required
def chatbot_api(request):
    user = request.user

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data["message"]
            name = data["name"]

            session_key = request.session.session_key
            if not session_key:
                request.session.save()
            session_key = request.session.session_key
            response = get_chatbot_response(message, session_key, user.pk, name)
            return JsonResponse({"message": response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except KeyError:
            return JsonResponse({"error": "Missing 'message' field in request body."}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)