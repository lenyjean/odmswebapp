from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name="home"),
    path('login', login_page, name="login"),
    path('logout', logout_page, name="login"),
    path('accounts-list', account, name="accounts-list"),
    path('create-new-account', add_account, name="create-new-account"),
    path('view-account/<str:pk>', view_account, name="view-account"),
    path('update-account/<str:pk>', update_account, name="update-account"),
    path('delete-account/<str:pk>', delete_account, name="delete-account"),
    path('category', category, name="category"),
    path('add-new-category', add_category, name="add-new-category"),
    path('update-category/<str:pk>', update_category, name="update-category"),
    path('delete-category/<str:pk>', delete_category, name="delete-category"),
    path('document', document, name="document"),
    path('add-new-document', add_docu, name="add-new-document"),
    path('view-document/<str:pk>', view_docu, name="view-document"),
    path('update-document/<str:pk>', update_docu, name="update-document"),
    path('delete-document/<str:pk>', delete_docu, name="delete-document"),
    path('activity-history', history, name="activity-history"),
    path('user-profile', view_profile, name="profile"),
    path('update-password', password_update, name="update-password"),
    
    path("department", department, name="department"),
    path("department/add", add_department, name="add_department"),
    path("department/update/<str:pk>", update_department, name="update_department"),
    path("department/delete/<str:pk>", delete_department, name="delete_department"),
]