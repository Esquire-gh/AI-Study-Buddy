"""
URL configuration for study_buddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chat.views import login, chat_interface, load_canvas_course_files, tokenize_selected_files, get_chatbot_response


admin.site.site_url = '/chat'
admin.site.site_header = 'AI Study Buddy'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login),
    path("chat/", chat_interface),
    path("load-course-files/", load_canvas_course_files),
    path("tokenize-files/", tokenize_selected_files),
    path('chat/get_chatbot_response/', get_chatbot_response, name='get_chatbot_response'),
]
