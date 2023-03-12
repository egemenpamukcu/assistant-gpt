from celery import shared_task
from .handlers.bio_handler import create_user_bio, save_bio

@shared_task
def generate_user_bio(messages, bio, user_social):
    user_bio = create_user_bio(messages, bio)
    print(user_bio)
    save_bio(user_social, user_bio)