from django.db import models
from django.conf import settings
from datetime import datetime, timedelta, date
from django.utils import timezone
from auth_user.models import *

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class CommonField(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        return self.title


class Course(CommonField):
    topic = models.CharField(max_length=100)


class Chapter(CommonField):
    picture = models.ImageField(upload_to="chapter-icon")
    time_to_complete = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Completed(models.Model):
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.first_name} - {self.chapter}"


class Content(models.Model):
    Type = models.CharField(
        max_length=255,
        choices=[
            ("heading", "heading"),
            ("text", "text"),
            ("image", "image"),
            ("audio", "audio"),
            ("video", "video"),
        ],
    )
    file = models.FileField(upload_to="content-files", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.chapter} - *{self.Type}*"

    class Meta:
        ordering = ("id",)


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.chapter} -> {self.name}"


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz} -> {self.title}"


class Option(models.Model):
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question} -> {self.answer} - {self.is_correct}"

    def save(self, *args, **kwargs):
        is_correct = self.is_correct
        if is_correct:
            all_options = Option.objects.filter(question=self.question)
            all_options.update(is_correct=False)
        self.is_correct = is_correct
        super(Option, self).save(*args, **kwargs)

    class Meta:
        ordering = ("id",)


class Review(models.Model):
    star = models.IntegerField()
    message = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
