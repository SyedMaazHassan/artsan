from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from auth_user.models import *


class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        errors = {}
        if "email" in data:
            email = data["email"]
            if "@artsenvanmorgen.nl" not in email:
                errors["email"] = "This email can't be registered."

        if "phone" in data:
            phone = data["phone"]
            phone = phone.replace("-", "")
            if not (phone.isnumeric() and (9 < len(phone) < 15)):
                errors["phone"] = "Enter a valid phone number"
        if len(errors.keys()) > 0:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = SystemUser
        exclude = ["id"]
