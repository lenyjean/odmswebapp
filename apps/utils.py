from .models import ActivityHistory

def create_history(user, history, user_image):
    ActivityHistory.objects.create(user=user, history=history, user_image=user_image)

def delete_history(user, history, user_image):
    ActivityHistory.objects.create(user=user, history=history, user_image=user_image)

def download_history(user, history, user_image):
    ActivityHistory.objects.create(user=user, history=history, user_image=user_image)