from django.db import models
import python_avatars as pa
from django.conf import settings
import string
import os
from datetime import datetime, timedelta, date
from django.utils import timezone
import uuid

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

# System user to save in database
class SystemUser(models.Model):
    uid = models.CharField(unique=True, max_length=255)
    avatar = models.CharField(
        max_length=255, null=True, blank=True, default="avatars/default-profile.png"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} - {self.uid}"

    def random_string_generator(self, str_size, allowed_chars):
        import random

        return "".join(random.choice(allowed_chars) for x in range(str_size))

    def add_avatar(self):
        chars = "ABCDEFG0123456789HIJKLMNOPQRSTU0123456789VWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        size = 12
        name = self.random_string_generator(size, chars)
        random_avatar = pa.Avatar(
            style=pa.AvatarStyle.CIRCLE,
            hair_color=pa.HairColor.pick_random(),
            background_color=pa.BackgroundColor.pick_random(),
            eyebrows=pa.EyebrowType.pick_random(),
            mouth=pa.MouthType.SMILE,
            eyes=pa.EyeType.DEFAULT,
            top=pa.HairType.pick_random(),
            nose=pa.NoseType.pick_random(),
            accessory=pa.AccessoryType.NONE,
            clothing=pa.ClothingType.HOODIE,
            clothing_color=pa.ClothingColor.pick_random(),
        )
        file_name_temp = name + ".svg"
        file_path = os.path.join(settings.BASE_DIR, "media", "avatars", file_name_temp)
        random_avatar.render(file_path)
        self.avatar = "/media/avatars/" + file_name_temp

    def save(self, *args, **kwargs):
        if not self.pk:
            self.add_avatar()
        super(SystemUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# API keys to save in database
class API_Key(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.key)

    class Meta:
        verbose_name = "API key"
        verbose_name_plural = "API keys"
