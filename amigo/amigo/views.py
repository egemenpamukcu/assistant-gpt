from django.shortcuts import render
from apps.user_profile.utils import create_user_profile_if_does_not_exist
from apps.chatbot.models import Bot

def home(request):
    if request.user.is_authenticated:
        create_user_profile_if_does_not_exist(
            request.user, 
            request.user.social_auth.get(provider='google-oauth2').extra_data)
        bots = Bot.objects.all()
        bot_links = []
        for bot in bots:
            bot_links.append({
                'name': bot.name,
                'url': f'/bot/?bot_id={bot.id}',
            })
        context = {'bot_links': bot_links}
        return render(request, 'home.html', context=context)
        
    return render(request, 'home.html')