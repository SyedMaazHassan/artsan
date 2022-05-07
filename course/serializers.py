from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from course.models import *
from django.db.models import Q
from auth_user.serializers import *


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        exclude = ("id", "course")


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        # fields = "__all__"
        exclude = ("question",)


class QuizResponseSerailizer(serializers.ModelSerializer):
    class Meta:
        model = QuizResponse
        # fields = "__all__"
        exclude = ("json", "quiz", "user", "id")


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField(method_name="get_options")

    class Meta:
        model = Question
        # fields = "__all__"
        exclude = ("quiz",)

    def get_options(self, instance):
        question_id = instance.id
        all_options = Option.objects.filter(question_id=question_id)
        serlaized_options = OptionSerializer(all_options, many=True).data
        return serlaized_options


class ContentSerializer(serializers.ModelSerializer):
    duration = serializers.CharField(source="get_duration")

    class Meta:
        model = Content
        # fields = "__all__"
        exclude = ("chapter", "id")


class ChapterSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField(method_name="get_is_completed")
    is_locked = serializers.SerializerMethodField(method_name="get_is_locked")

    def get_is_completed(self, instance):
        chapter_id = instance.id
        user = self.context["user"]
        return Completed.objects.filter(user=user, chapter_id=chapter_id).exists()

    def get_is_locked(self, instance):
        chapter = instance
        user = self.context["user"]
        all_completed = Completed.objects.filter(user=user).values_list(
            "chapter_id", flat=True
        )
        all_chapters_not_completed = Chapter.objects.filter(course=chapter.course)
        all_chapters_not_completed = all_chapters_not_completed.filter(
            ~Q(id__in=all_completed)
        )
        if all_chapters_not_completed.count() > 0:
            if (
                all_chapters_not_completed[0].id == instance.id
                or instance.id in all_completed
            ):
                return False
            return True
        else:
            return False

    class Meta:
        model = Chapter
        exclude = ("course",)


class CourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField(method_name="get_progress")

    def get_progress(self, instance):
        course_id = instance.id
        user = self.context["user"]
        all_completed_chapters = Completed.objects.filter(user=user).values_list(
            "chapter_id", flat=True
        )
        all_chapters = Chapter.objects.filter(course_id=course_id)
        all_remaining_chapters = all_chapters.filter(~Q(id__in=all_completed_chapters))
        all_remaining_count = all_remaining_chapters.count()
        next_chapter_to_open = (
            all_remaining_chapters[0].id if all_remaining_count > 0 else None
        )
        all_count = all_chapters.count()
        completed_count = all_count - all_remaining_count
        if all_count != 0:
            percent_progress = int(completed_count / all_count * 100)
            status = (
                "Course completed"
                if all_remaining_count == 0
                else f"Chapter {completed_count + 1} out of {all_count}"
            )
            return {
                "progress": percent_progress,
                "status": status,
                "open_id": next_chapter_to_open,
            }
        return None

    class Meta:
        model = Course
        fields = "__all__"
