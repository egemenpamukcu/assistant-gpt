from django.contrib.auth import get_user_model
from .openai_handler import get_assistant_message

User = get_user_model()

def get_bio(pk):
    user = User.objects.get(pk=pk)
    return user.bio
    
def save_bio(pk, bio):
    user = User.objects.get(pk=pk)
    user.bio = bio
    user.save()

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