from django.shortcuts import render, redirect

def login(request):
    
        
    return render(request, "login.html")


def chatbox(request):
    return render(request, "chatbox.html")