import json

from django.shortcuts import render
from chat.utils.canvas_client import get_canvas_client
from django.http import JsonResponse



def login(request):
    return render(request, "login.html")


def load_canvas_course_files(request):
    course_files = []

    canvas_client = get_canvas_client(request.user)
    course_reponse = canvas_client.courses()

    if course_reponse:
        courses = course_reponse.json()

        for course in courses:
            course_dict = {
                "id": course["id"],
                "name": course["name"],
                "files": []
            }
            course_files_response = canvas_client.course_files(course["id"])
            if course_files_response:
                for file in course_files_response.json():
                    course_dict["files"].append(
                        {
                            "id": file["id"],
                            "name": file["display_name"],
                            "url": file["url"],
                        }
                    )
            course_files.append(course_dict) 
    return JsonResponse({'course_files': course_files})


def chat_interface(request):
    # get all converstations
    # get all courses and their files
    # if conversation is selected
        # get the converstation
        # get the conversation context files and thier courses and update the course files

    context = {
        "conversations": [],
        "course_files": [],
    }
    return render(request, "chatbox.html", context=context)
