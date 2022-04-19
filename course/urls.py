from django.urls import path
from . import views
from course.views import *

urlpatterns = [
    # Users
    path("course", CourseApi.as_view()),
    path("course/<id>", CourseApi.as_view()),
]
