from django.contrib.sessions.backends.db import SessionStore
from .bio_handler import get_bio
from .openai_handler import get_assistant_message
from .bot_handler import get_bot_prompt
from .bio_handler import create_user_bio, save_bio


def get_chatbot_response(message, session_key, pk, bot_name):
    session = SessionStore(session_key=session_key)

    bio = get_bio(pk)

    prompt = f"""{get_bot_prompt(bot_name)}
    Here are some details that we already know about them: 
    
    {bio}"""

    messages = session.get(f'messages{pk}', [
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "Hey, how are you today! :)"},
            ])


    messages.append({"role": "user", "content": message})

    if (len(messages) % 5 == 0):
        bio_messages = messages[3:] # Strip the prompt messages.
        user_bio = create_user_bio(bio_messages, bio)
        print(user_bio)
        save_bio(pk, user_bio)

    messages.append({"role": "assistant", "content": get_assistant_message(messages)})

    session[f'messages{pk}'] = messages
    session.save()

    return messages[-1]['content']