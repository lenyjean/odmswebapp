from django.urls import path
from .views import *

urlpatterns = [
    # These are URL patterns defined using Django's `path` function.
    path('', homepage, name="home"),
    path('login', login_page, name="login"),
    path('logout', logout_page, name="login"),

   # These are URL patterns for handling different account-related views in a Django web application.
    path('account', account, name="account"),
    path('account/add', add_account, name="add_account"),
    path('account/view/<str:pk>', view_account, name="view_account"),
    path('account/update/<str:pk>', update_account, name="update_account"),
    path('account/delete/<str:pk>', delete_account, name="delete_account"),

    # These are URL patterns for handling different category-related views in a Django web
    # application.
    path('category', category, name="category"),
    path('category/add', add_category, name="add_new_category"),
    path('category/update/<str:pk>', update_category, name="update_category"),
    path('category/delete/<str:pk>', delete_category, name="delete_category"),

    # These are URL patterns for handling different document-related views in a Django web
    # application. The `path` function is used to define the URL pattern, followed by the name of the
    # view function that will handle the request, and a unique name for the URL pattern. The different
    # URL patterns include:
    path('document', document, name="document"),
    path('document/add', add_docu, name="add_new_document"),
    path('document/view/<str:pk>', view_docu, name="view_document"),
    path('document/update/<str:pk>', update_docu, name="update_document"),
    path('document/delete/<str:pk>', delete_docu, name="delete_document"),
    path('document/forward/<str:pk>', send_docu, name="forward_document"),

    # `path('activity/history', history, name="activity_history")` is defining a URL pattern for the
    # `history` view function, which will handle requests to the `/activity/history` URL. The `name`
    # parameter is used to give a unique name to the URL pattern, which can be used to refer to it in
    # other parts of the Django application.
    path('activity/history', history, name="activity_history"),

   # `path('profile', view_profile, name="profile")` is defining a URL pattern for the `view_profile`
   # view function, which will handle requests to the `/profile` URL. The `name` parameter is used to
   # give a unique name to the URL pattern, which can be used to refer to it in other parts of the
   # Django application.
    path('profile', view_profile, name="profile"),

    # `path('update/password', password_update, name="update_password")` is defining a URL pattern for
    # the `password_update` view function, which will handle requests to the `/update/password` URL.
    # The `name` parameter is used to give a unique name to the URL pattern, which can be used to
    # refer to it in other parts of the Django application. This URL pattern is used to handle
    # requests for updating the user's password.
    path('update/password', password_update, name="update_password"),
    
   # These are URL patterns for handling different department-related views in a Django web
   # application. The `path` function is used to define the URL pattern, followed by the name of the
   # view function that will handle the request, and a unique name for the URL pattern. The different
   # URL patterns include:
    path("department", department, name="department"),
    path("department/add", add_department, name="add_department"),
    path("department/update/<str:pk>", update_department, name="update_department"),
    path("department/delete/<str:pk>", delete_department, name="delete_department"),
]