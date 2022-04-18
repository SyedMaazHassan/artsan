from django.urls import path
from . import views
from course.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Users
    path("course", CourseApi.as_view()),
    path("course/<id>", CourseApi.as_view()),
]


urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
