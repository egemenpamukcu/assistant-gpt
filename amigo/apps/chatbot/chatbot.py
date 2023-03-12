import os
from dotenv import load_dotenv
import openai
from django.contrib.sessions.backends.db import SessionStore
from .models import UserBio
from .models import Bot
from .tasks import generate_user_bio


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')    

def get_bio(user_social):
    try:
        user_bio = UserBio.objects.get(user_social=user_social)
        return user_bio.bio
    except UserBio.DoesNotExist:
        return """Name: Unknown

        Age: Unknown

        Occupation: Unknown

        Interests: Unknown

        Personality traits: Unknown

        Other relevant information: Unknown."""
    
def save_bio(user_social, bio):
    try:
        user = UserBio.objects.get(user_social=user_social)
        user.bio = bio
        user.save()
    except UserBio.DoesNotExist:
        UserBio.objects.create(user_social=user_social, bio=bio)

def get_chatbot_prompt(bot_name):
    try:
        bot = Bot.objects.get(name=bot_name)
        return bot.prompt
    except Bot.DoesNotExist:
        raise ValueError(f"No Bot object found with name {bot_name}")

def get_chatbot_response(message, session_key, user_social, bot_name):
    session = SessionStore(session_key=session_key)

    bio = get_bio(user_social)

    prompt = f"""{get_chatbot_prompt(bot_name)}
    Here are some details that we already know about them: 
    
    {bio}"""

    messages = session.get(f'messages{user_social}', [
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "Hey, how are you today! :)"},
            ])


    messages.append({"role": "user", "content": message})

    if (len(messages) % 5 == 0):
        bio_messages = messages[3:] # Strip the prompt messages.
        generate_user_bio.delay(bio_messages, bio, user_social)

    messages.append({"role": "assistant", "content": get_assistant_message(messages)})

    session[f'messages{user_social}'] = messages
    session.save()

    return messages[-1]['content']

def get_assistant_message(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )

    assistant_message = response['choices'][0]['message']['content']

    return assistant_message

def get_bio_creation_prompt(bio, messages):
    return f"""Generate a new bio for the user based on the following information:

                {bio}

                New chat log:
                {str(messages)}

                Please generate a new bio for the user that incorporates information from both the previous bio and the new chat log. 
                The new bio should include all of the known information from the previous bio, as well as any new information that was revealed in the chat log. 
                For example, if the bio states "Name: Unknown", and they state that their name is Josh, write out "Name: Josh"  
                Even if the new information seems unrelated to the existing information, it is important that you include all of the known information from the previous bio in the new bio. 
                If a field is already filled in, append any new information to the end of the field, separated by a semicolon (;). 
                If the information is not available in the chat log, leave the field blank.
                """

def create_user_bio(messages, bio):
    prompt = get_bio_creation_prompt(bio, messages)
    
    m = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt},

        ]
    return get_assistant_message(m)

def get_assistant_message(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )

    assistant_message = response['choices'][0]['message']['content']

    return assistant_message