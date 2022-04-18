from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from auth_user.authentication import RequestAuthentication, ApiResponse
from auth_user.serializers import *
from auth_user.support import *

# Create your views here.


class UserApi(APIView, ApiResponse):
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

    def get(self, request, uid=None):
        try:
            if not uid:
                user_object = SystemUser.objects.all()
                many = True
            else:
                user_object = get_object_or_404(SystemUser, uid=uid)
                many = False
            serializer = UserSerializer(user_object, many=many)
            self.postSuccess({"users": serializer.data}, "User fetched successfully")
        except Exception as e:
            self.postError({"users": str(e)})
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
