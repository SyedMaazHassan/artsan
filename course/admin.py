from django.contrib import admin
from course.models import *
from pyexpat import model


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]


class ContentInline(admin.StackedInline):
    model = Content
    extra = 1


class ChapterAdmin(admin.ModelAdmin):
    inlines = [ContentInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Content)
# admin.site.register(Completed)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizResponse)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Review)
