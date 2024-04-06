from django.db import models
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    canvas_api_token = models.CharField(max_length=200)
