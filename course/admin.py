from django.contrib import admin
from course.models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Content)
admin.site.register(Completed)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
