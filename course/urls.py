from django.urls import path
from . import views
from course.views import *

urlpatterns = [
    # Users
    path("", index, name="index"),
    path("course", CourseApi.as_view()),
    path("course/<id>", CourseApi.as_view()),
    path("chapter/<id>", ChapterApi.as_view()),
    path("quiz/<id>", QuizApi.as_view()),
]
