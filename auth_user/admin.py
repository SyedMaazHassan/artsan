from django.contrib import admin
from auth_user.models import *
from pyexpat import model

# Register your models here.


admin.site.register(SystemUser)
admin.site.register(API_Key)
