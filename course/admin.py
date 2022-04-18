from django.contrib import admin
from course.models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Completed)
