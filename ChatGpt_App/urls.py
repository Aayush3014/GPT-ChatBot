from django.urls import path
from ChatGpt_App import views


urlpatterns = [
    path("", views.chatbot, name="chatbot"),
]
