# Generated by Django 4.2.2 on 2023-08-08 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_useractionlog_target_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceCapture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capture', models.ImageField(blank=True, max_length=255, null=True, upload_to='datacapture/', verbose_name='Face Capture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Face Capture',
                'verbose_name_plural': 'Faces Capture',
            },
        ),
    ]