from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Chat

from django.utils import timezone
# Create your views here.


openai_api_key = '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'

openai.api_key = openai_api_key


def ask_response(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer



def chatbot(request):   
    chats = Chat.objects.filter(user=request.user)
    if request.method == "POST":
        message = request.POST.get('message')
        response = ask_response(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html",{'chats':chats})

    


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid Credentials"
            return render(request, "login.html", {"error": error_message})
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if password1 == password2:

            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = "Error Creating Account"
                return render(request, "register.html", {"error": error_message})
        else:
            error_message = "Password does not match"
            return render(request, "register.html", {"error": error_message})
    
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")