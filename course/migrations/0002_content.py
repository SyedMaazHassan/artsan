# Generated by Django 4.0.4 on 2022-04-19 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('heading', 'heading'), ('text', 'text'), ('image', 'image'), ('audio', 'audio'), ('video', 'video')], max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to='content-files')),
                ('text', models.TextField(blank=True, null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.chapter')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]