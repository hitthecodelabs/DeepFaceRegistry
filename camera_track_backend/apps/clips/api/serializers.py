from camera_track.settings.base import MEDIA_URL
from rest_framework.serializers import (ModelSerializer, FileField,
                                        SerializerMethodField, ValidationError)

from apps.base.serializers import BaseHistoricGroupByMonthSerializer
from apps.clips.models import Clip


class ClipSerializer(ModelSerializer):
    file = FileField()
    name = SerializerMethodField()
    size = SerializerMethodField()

    class Meta:
        model = Clip
        exclude = ('state', 'modified_date', 'deleted_date')

    def validate_file(self, value):
        name = value.name
        name_evaluation = name.split('.')
        file_ext = name_evaluation[1].lower()
        print(file_ext)
        if file_ext != 'avi' and file_ext != 'mp4':
            raise ValidationError(
                "El fichero solo puede ser de extensión '.avi' o '.mp4'")
        size = value.size / (1024 * 1024)
        if size <= 0:
            raise ValidationError("El fichero tiene un peso menor a cero.")
        return value

    # def to_internal_value(self, data):
    #     print('Deserializing data:', data)
    #     return super().to_internal_value(data)

    def create(self, validated_data):
        file_obj = validated_data.get('file')
        camera_id = validated_data.get('camera')
        name = file_obj.name
        # convert to MB
        size = file_obj.size / (1024 * 1024)

        # SAVE THE MODEL

        # CREATE THE OBJECT WITH THE PROCESSED DATA
        clip = Clip.objects.create(name=name,
                                   file=file_obj,
                                   size=size,
                                   camera=camera_id)

        return clip


class ClipListSerializer(ModelSerializer):
    class Meta:
        model = Clip
        exclude = ('state', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        file_url = 'http://localhost:8000' + MEDIA_URL + instance.file.name

        data = {
            'id': instance.id,
            'name': instance.name,
            # 'file': self.context['request'].build_absolute_uri(instance.file.url),
            'file': file_url,
            'size': instance.size,
            'created_date': instance.created_date,
            'camera_id': instance.camera.id,
            'camera_name': instance.camera.name,
            'camera_ip': instance.camera.ip
        }

        return data


class ClipHistoricGroupByMonthSerializer(BaseHistoricGroupByMonthSerializer):

    class Meta:
        model = Clip
        fields = ('month', 'total')
