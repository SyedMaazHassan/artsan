# Generated by Django 4.0.4 on 2022-04-23 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0002_systemuser_is_font_large_systemuser_is_light_theme_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemuser',
            name='theme',
        ),
    ]