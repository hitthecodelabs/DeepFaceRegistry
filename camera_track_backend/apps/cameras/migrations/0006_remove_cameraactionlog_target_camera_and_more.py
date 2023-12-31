# Generated by Django 4.1.7 on 2023-06-20 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0005_cameraactionlog_delete_historicalcamera'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cameraactionlog',
            name='target_camera',
        ),
        migrations.RemoveField(
            model_name='cameraactionlog',
            name='user',
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='cam_file',
            field=models.CharField(blank=True, default='/camera', max_length=200, null=True, verbose_name='Extensión'),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='cam_id',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='cam_password',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Contrasena Camara'),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='cam_port',
            field=models.IntegerField(default=443, verbose_name='Puerto'),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='cam_username',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Usuario Camara'),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='user_email',
            field=models.EmailField(default='no_reply@domain.com', max_length=255, verbose_name='Correo Electrónico'),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='user_id',
            field=models.BigIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='cameraactionlog',
            name='username',
            field=models.CharField(default='john_doe', max_length=255),
        ),
    ]
