from django.conf import settings
from django.db import models

from apps.base.models import BaseModel


# Create your models here.
class Camera(BaseModel):
    ip = models.CharField('ip', max_length=16, blank=False,
                          null=False, unique=False)
    name = models.CharField('Nombre', max_length=100, blank=False, null=False)
    port = models.IntegerField('Puerto', blank=False, null=False, default=443)
    file = models.CharField('Extensión', max_length=200, blank=True, null=True, default='/camera')
    cam_username = models.CharField('Usuario Camara', max_length=150, blank=True, null=True)
    cam_password = models.CharField('Contrasena Camara', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Cámara'
        verbose_name_plural = 'Cámaras'

    def __str__(self) -> str:
        return f'{self.name}: {self.ip}'

    def link_live_stream(self) -> str:
        if self.cam_username != '' and self.cam_password != '':
            link = f"rtsp://{self.cam_username}:{self.cam_password}@{self.ip}:{self.port}{self.file}"
        else:
            link = f"rtsp://{self.ip}:{self.port}{self.file}"
        return link


class CameraActionLog(models.Model):
    ACTION_CHOICES = [
        ('C', 'Create'),
        ('U', 'Update'),
        ('D', 'Delete'),
    ]
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE),
    user_id = models.BigIntegerField(default=-1)
    username = models.CharField(max_length=255, default='john_doe')
    user_email = models.EmailField('Correo Electrónico', max_length=255, default='no_reply@domain.com')
    action = models.CharField(choices=ACTION_CHOICES, max_length=1)
    # camera_id = models.ForeignKey(Camera,
    #                                   on_delete=models.CASCADE)
    cam_id = models.BigIntegerField(default=-1)
    cam_name = models.CharField('Nombre', max_length=100, null=False, default='empty_space')
    cam_ip = models.CharField('ip', max_length=16, null=False, default='255.255.255.255')
    cam_port = models.IntegerField('Puerto', blank=False, null=False, default=443)
    cam_file = models.CharField('Extensión', max_length=200, blank=True, null=True, default='/camera')
    cam_username = models.CharField('Usuario Camara', max_length=150, blank=True, null=True)
    cam_password = models.CharField('Contrasena Camara', max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
