from django.db import models

from apps.base.models import BaseModel
from apps.cameras.models import Camera


# Create your models here.
class Clip(BaseModel):
    name = models.CharField('nombre', max_length=200, blank=False, null=False)
    # path = models.CharField('ruta', max_length=200, blank=False, null=False)
    file = models.FileField(upload_to='%Y-%m-%d/')
    size = models.IntegerField('peso', blank=False, null=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, verbose_name='Cámara', blank=False, null=False)

    class Meta:
        verbose_name = 'Clip'
        verbose_name_plural = 'Clips'

    def __str__(self) -> str:
        return f'{self.name}'


# class ClipActionLog(models.Model):
#     ACTION_CHOICES = [
#         ('C', 'Create'),
#         ('U', 'Update'),
#         ('D', 'Delete'),
#     ]
#     camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='actions')
#     action = models.CharField(choices=ACTION_CHOICES, max_length=1)
#     timestamp = models.DateTimeField(auto_now_add=True)
