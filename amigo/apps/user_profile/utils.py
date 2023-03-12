from .models import UserProfile

def create_user_profile_if_does_not_exist(user, social):
    try:
        profile = UserProfile.objects.filter(email=user.email)
        return profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user, user_social=social)
        profile.save()
        return profile