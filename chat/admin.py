from django.contrib import admin
from chat.models import UserProfile, Course, CourseFile, Conversation, Message

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseFile)
class CourseProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Conversation)
class CourseProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class CourseProfileAdmin(admin.ModelAdmin):
    pass
