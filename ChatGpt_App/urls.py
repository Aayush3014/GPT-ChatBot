from django.urls import path
from ChatGpt_App import views


urlpatterns = [
    path("", views.chatbot, name="chatbot"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
]
