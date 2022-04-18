from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from auth_user.authentication import RequestAuthentication, ApiResponse
from course.serializers import *

# Create your views here.


class CourseApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def post(self, request, uid=None):
        try:
            data = request.data.copy()
            data["uid"] = uid
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user = SystemUser.objects.get(uid=uid)
                self.postSuccess({"user": serializer.data}, "User added successfully")
            else:
                self.postError(beautify_errors(serializer.errors))
        except Exception as e:
            self.postError({"uid": str(e)})
        return Response(self.output_object)

    def get(self, request, id=None):
        try:
            user = SystemUser.objects.get(uid=request.headers["uid"])
            print(user)
            if not id:
                course_object = Course.objects.all()
                many = True
            else:
                course_object = get_object_or_404(Course, id=id)
                many = False

            serializer = CourseSerializer(
                course_object, many=many, context={"user": user}
            )
            self.postSuccess({"course": serializer.data}, "Course fetched successfully")
        except Exception as e:
            self.postError({"course": str(e)})
        return Response(self.output_object)

    def patch(self, request, uid=None):
        try:
            user_obj = get_object_or_404(SystemUser, uid=uid)
            if "email" in request.data and user_obj.email != request.data["email"]:
                self.postError(
                    {
                        "email": "To avoid problems with future signin, Email cannot be updated"
                    }
                )
                return Response(self.output_object)

            serializer = UserSerializer(user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                self.postSuccess({"user": serializer.data}, "User updated successfully")
            else:
                self.postError(beautify_errors(serializer.errors))
        except Exception as e:
            self.postError({"uid": str(e)})
        return Response(self.output_object)
