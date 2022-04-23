# Generated by Django 4.0.4 on 2022-04-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemuser',
            name='is_font_large',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='is_light_theme',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='theme',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]