from django.urls import path
from . import views
from auth_user.views import *

urlpatterns = [
    # Users
    path("user", UserApi.as_view()),
    path("user/<uid>", UserApi.as_view()),
]
