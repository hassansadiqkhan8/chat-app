from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.user_registration, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("", views.home, name="home"),
    
    path("chat/<str:pk>/", views.chat_details, name="chat"),
    path("new-chat/", views.new_chat, name="new-chat"),
]