from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from course.models import *
from django.db.models import Q


class ChapterSerializer(serializers.ModelSerializer):
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
            return
        return None

    class Meta:
        model = Course
        fields = "__all__"
