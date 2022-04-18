from django.urls import path
from . import views
from auth_user.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Users
    path("user", UserApi.as_view()),
    path("user/<uid>", UserApi.as_view()),
]


urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
