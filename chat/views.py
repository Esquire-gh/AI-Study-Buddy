import json

from django.shortcuts import render
from chat.utils.canvas_client import get_canvas_client
from django.http import JsonResponse

from chat.models import Course, CourseFile, Conversation



def login(request):
    return render(request, "login.html")


def load_canvas_course_files(request):
    canvas_client = get_canvas_client(request.user)
    course_reponse = canvas_client.courses()

    if course_reponse:
        courses = course_reponse.json()

        for course in courses:
            course_obj, _ = Course.objects.update_or_create(
                user=request.user, 
                external_id=course["id"],
                defaults={
                    "name": course["name"],
                }
            )

            course_files_response = canvas_client.course_files(course["id"])
            if course_files_response:
                for file in course_files_response.json():
                    course_file, _ = CourseFile.objects.update_or_create(
                        course=course_obj,
                        external_id=file["id"],
                        defaults={
                            "name": file["display_name"],
                            "url": file["url"],
                        }
                    )
    return JsonResponse({})


def tokenize_selected_files(request):
    return JsonResponse({})


def chat_interface(request):
    convos = Conversation.objects.filter(user=request.user).values("id", "title")
    courses = Course.objects.prefetch_related('coursefile_set').filter(user=request.user).all()

    course_files = []

    for course in courses:
        course_dict = {
            "course_id": course.id,
            "course_name": course.name,
            "files": []
        }

        for file in course.coursefile_set.all():
            course_dict["files"].append(
                {
                    "id": file.id,
                    "name": file.name,
                    "url": file.url
                }
            )

        course_files.append(course_dict)

    context = {
        "conversations": convos,
        "messages": [],
        "course_files": course_files,
    }
    return render(request, "chatbox.html", context=context)


def chat_detail(request, chat_id):
    convos = Conversation.objects.filter(user=request.user).values("id", "title")
    courses = Course.objects.prefetch_related('coursefile_set').filter(user=request.user).all()

    course_files = []

    for course in courses:
        course_dict = {
            "course_id": course.id,
            "course_name": course.name,
            "files": []
        }

        for file in course.coursefile_set.all():
            course_dict["files"].append(
                {
                    "id": file.id,
                    "name": file.name,
                    "url": file.url
                }
            )

        course_files.append(course_dict)

    context = {
        "conversations": convos,
        "current_conversation_messages": [],
        "course_files": course_files,
    }
    return render(request, "chatbox.html", context=context)


def get_chatbot_response(request):
    user_message = "ChatGPT"
    bot_response = f"Simulated ChatGPT response to '{user_message}'"
    
    return JsonResponse({'bot_response': bot_response})
