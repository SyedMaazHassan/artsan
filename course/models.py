from django.db import models
from django.conf import settings
from datetime import datetime, timedelta, date
from django.utils import timezone
from auth_user.models import *
import json, os

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

    def markAsCompleted(self, user):
        check_query = Completed.objects.filter(chapter=self, user=user).exists()
        if not check_query:
            Completed.objects.create(chapter=self, user=user)


class Completed(models.Model):
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.full_name} - {self.chapter}"


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

    def duration_detector(self, length):
        hours = length // 3600  # calculate in hours
        length %= 3600
        mins = length // 60  # calculate in minutes
        length %= 60
        seconds = length  # calculate in seconds

        return hours, mins, seconds

    def audio_duration(self, length):
        hours = length // 3600  # calculate in hours
        length %= 3600
        mins = length // 60  # calculate in minutes
        length %= 60
        seconds = length  # calculate in seconds
        return hours, mins, seconds

    def get_duration(self):
        import mutagen

        if self.Type not in ["audio", "video"]:
            return None

        audio_info = mutagen.File(self.file).info
        hours, mins, seconds = self.audio_duration(int(audio_info.length))
        return f"{hours}:{mins}:{seconds}"

    def __str__(self):
        return f"{self.chapter} - *{self.Type}*"

    class Meta:
        ordering = ("id",)


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.chapter} -> {self.name}"


class QuizResponse(models.Model):
    json = models.TextField()
    result = models.FloatField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def calculate_result(self, response):
        response_length = len(response)
        all_questions = Question.objects.filter(quiz=self.quiz)
        all_questions_ids = all_questions.values_list("id", flat=True)
        total_questions = all_questions_ids.count()
        correct_answers = 0

        if response_length == 0 or response_length != total_questions:
            raise Exception("Invalid quiz response")

        all_answers = Option.objects.filter(question_id__in=all_questions_ids)
        for single_response in response:
            question = all_questions.filter(id=single_response["question_id"]).first()
            if question:
                answer = all_answers.filter(
                    question=question, id=single_response["answer_id"]
                ).first()
                if answer:
                    if answer.is_correct:
                        correct_answers += 1
                else:
                    raise Exception("Provided quiz response has invalid answer_id")
            else:
                raise Exception("Provided quiz response has invalid question_id")
        result = round(correct_answers / total_questions * 100, 2)
        self.result = result
        self.json = json.dumps(response)

    def __str__(self):
        return f"Response: {self.quiz} => {self.user}"


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

    def __str__(self):
        return f"{self.course} - *{self.star}* - *{self.message}* -  *{self.user.full_name}*"
