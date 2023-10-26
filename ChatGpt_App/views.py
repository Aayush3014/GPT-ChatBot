from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.


openai_api_key = 'Your_API_Key'

openai.api_key = openai_api_key


def ask_response(message):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = message,
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature = 0.7,
    )

    
    answer = response.choices[0].text.strip()
    return answer



def chatbot(request):

    if request.method == "POST":
        message = request.POST.get('message')
        response = ask_response(message)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html")

    


def login(request):
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