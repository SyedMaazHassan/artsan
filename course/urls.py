from django.urls import path
from . import views
from auth_user.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = []


urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
