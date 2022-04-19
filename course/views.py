from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from auth_user.authentication import RequestAuthentication, ApiResponse
from course.serializers import *

# Create your views here.
def index(request):
    chapter_id = 1
    all_content = Content.objects.filter(chapter_id=chapter_id)
    context = {"all_content": all_content}
    return render(request, "index.html", context)


class QuizApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def get_all_questions(self, quiz):
        all_questions = Question.objects.filter(quiz=quiz)
        serialized_all_questions = QuestionSerializer(all_questions, many=True).data
        return serialized_all_questions

    def get(self, request, id):
        try:
            output = {}
            user = SystemUser.objects.get(uid=request.headers["uid"])
            quiz_object = get_object_or_404(Quiz, id=id)
            output["quiz"] = {
                "name": quiz_object.name,
                "questions": self.get_all_questions(quiz_object),
            }
            self.postSuccess(output, "Quiz fetched successfully")
        except Exception as e:
            self.postError({"quiz": str(e)})
        return Response(self.output_object)


class ChapterApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def get_all_content(self, chapter):
        all_content = Content.objects.filter(chapter=chapter)
        serialized_all_content = ContentSerializer(all_content, many=True)
        return serialized_all_content.data

    def get(self, request, id):
        try:
            output = {}
            user = SystemUser.objects.get(uid=request.headers["uid"])
            print("=======")
            print(id)
            print("=======")
            chapter_object = get_object_or_404(Chapter, id=id)
            quiz = Quiz.objects.filter(chapter=chapter_object).first()
            all_content = self.get_all_content(chapter_object)
            output["chapter"] = ChapterSerializer(
                chapter_object, many=False, context={"user": user}
            ).data
            output["content"] = all_content
            output["quiz_id"] = quiz.id if quiz else None
            self.postSuccess(output, "Chapter fetched successfully")
        except Exception as e:
            self.postError({"chapter": str(e)})
        return Response(self.output_object)


class CourseApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def get_all_chapters(self, course, user):
        all_chapters = Chapter.objects.filter(course=course)
        serialized_all_chapters = ChapterSerializer(
            all_chapters, many=True, context={"user": user}
        )
        return serialized_all_chapters.data

    # def post(self, request, uid=None):
    #     try:
    #         data = request.data.copy()
    #         data["uid"] = uid
    #         serializer = UserSerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             user = SystemUser.objects.get(uid=uid)
    #             self.postSuccess({"user": serializer.data}, "User added successfully")
    #         else:
    #             self.postError(beautify_errors(serializer.errors))
    #     except Exception as e:
    #         self.postError({"uid": str(e)})
    #     return Response(self.output_object)

    def get(self, request, id=None):
        try:
            output = {}
            user = SystemUser.objects.get(uid=request.headers["uid"])
            if not id:
                course_object = Course.objects.all()
                many = True
            else:
                course_object = get_object_or_404(Course, id=id)
                many = False
                output["chapters"] = self.get_all_chapters(course_object, user)

            serialized_course = CourseSerializer(
                course_object, many=many, context={"user": user}
            )
            output["course"] = serialized_course.data
            self.postSuccess(output, "Course fetched successfully")
        except Exception as e:
            self.postError({"course": str(e)})
        return Response(self.output_object)

    # def patch(self, request, uid=None):
    #     try:
    #         user_obj = get_object_or_404(SystemUser, uid=uid)
    #         if "email" in request.data and user_obj.email != request.data["email"]:
    #             self.postError(
    #                 {
    #                     "email": "To avoid problems with future signin, Email cannot be updated"
    #                 }
    #             )
    #             return Response(self.output_object)

    #         serializer = UserSerializer(user_obj, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             self.postSuccess({"user": serializer.data}, "User updated successfully")
    #         else:
    #             self.postError(beautify_errors(serializer.errors))
    #     except Exception as e:
    #         self.postError({"uid": str(e)})
    #     return Response(self.output_object)
