from django.shortcuts import render, redirect
from django.http import JsonResponse

def login(request):
    
        
    return render(request, "login.html")


def chatbox(request):

    return render(request, "chatbox.html", {'username': request.user.username})

def get_chatbot_response(request):
    user_message = "ChatGPT"
    bot_response = f"Simulated ChatGPT response to '{user_message}'"
    
    return JsonResponse({'bot_response': bot_response})
