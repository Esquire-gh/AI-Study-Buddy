# chat/routing.py
from django.urls import re_path

from . import messages

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<username>\w+)/$", messages.ChatGPT.as_asgi()),
]