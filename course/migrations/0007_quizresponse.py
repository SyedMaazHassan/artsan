# Generated by Django 4.0.4 on 2022-04-20 11:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
        ('course', '0006_quiz_question_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.TextField()),
                ('result', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_user.systemuser')),
            ],
        ),
    ]