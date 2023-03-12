from ..models import Bot

def get_bot_prompt(bot_name):
    try:
        bot = Bot.objects.get(name=bot_name)
        return bot.prompt
    except Bot.DoesNotExist:
        raise ValueError(f"No Bot object found with name {bot_name}")