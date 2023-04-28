from .models import ActivityHistory

def create_history(user, history, user_image):
    """
    This function creates a new activity history object with the given user, history, and user image.
    
    :param user: The user parameter is an instance of the User model, which represents a user in the
    system. It contains information such as the user's username, email, password, and other details
    :param history: The "history" parameter is likely a string or text field that represents the
    activity or event that the user is creating a history for. It could be something like "completed a
    task" or "made a purchase". This parameter is used to create a new instance of the ActivityHistory
    model in the database
    :param user_image: The user_image parameter is likely an image file that represents the user. It
    could be a profile picture or any other image associated with the user. The function creates an
    instance of the ActivityHistory model with the provided user, history, and user_image parameters
    """
    ActivityHistory.objects.create(user=user, history=history, user_image=user_image)
    

def delete_history(user, history, user_image):
    """
    This function creates a new activity history object with the given user, history, and user image.
    
    :param user: The user parameter is an object that represents the user whose activity history is
    being deleted. It could be a Django User object or any other custom user model object
    :param history: The history parameter is likely a string or a list of strings that represents the
    activity or activities that the user wants to delete from their activity history. It could include
    things like search queries, viewed pages, or other actions taken on the website or application
    :param user_image: The user_image parameter is likely an image file associated with the user's
    account. It could be used to display the user's profile picture or to provide visual context for
    their activity history
    """
    ActivityHistory.objects.create(user=user, history=history, user_image=user_image)


def download_history(user, history, user_image):
    """
    This function creates a new activity history object with the given user, history, and user image.
    
    :param user: The user object represents the user who performed the activity that is being saved in
    the activity history. It could be an instance of a Django User model or a custom user model
    :param history: The "history" parameter is likely a string or a JSON object that represents the
    user's activity history. This could include information such as the user's login/logout times, pages
    visited, actions taken, etc
    :param user_image: The user_image parameter is likely an image file that represents the user. It
    could be a profile picture or any other image associated with the user. The function creates a new
    ActivityHistory object and saves it to the database with the provided user, history, and user_image
    parameters
    """
    ActivityHistory.objects.create(user=user, history=history, user_image=user_image)