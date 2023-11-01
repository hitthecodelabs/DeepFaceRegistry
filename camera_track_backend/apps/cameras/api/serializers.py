from datetime import datetime
from ipaddress import ip_address
from rest_framework.serializers import (ModelSerializer, ValidationError)
# from simple_history.models import HistoryMan

from apps.base.serializers import BaseHistoricGroupByMonthSerializer
from apps.cameras.models import Camera, CameraActionLog


class CameraSerializer(ModelSerializer):
    class Meta:
        model = Camera
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def validate_ip(self, value):
        # TODO: CHECK IF THE IP IS ACTIVE WITH PING OR EQUIVALENT
        # TODO: SHOULD BE ON CREATE
        try:
            ip_address(value)
        except ValueError:
            print("Invalid IP address")
            raise ValidationError('La ip ingresada no es válida.')
        return value

    def validate_port(self, value):
        try:
            int(value)
        except ValueError as e:
            print(f"{str(e)}")
            raise ValidationError('El valor del puerto es incorrecto')
        else:
            if value < 0:
                raise ValidationError('El valor no puede ser menor que cero.')
        return value


class CameraHistoricGroupByMonthSerializer(BaseHistoricGroupByMonthSerializer):

    class Meta:
        model = Camera
        fields = ('month', 'total')


class CameraHistoricSerializer(ModelSerializer):
    class Meta:
        model = CameraActionLog
        fields = '__all__'

    def get_action_described(self, action: str) -> str:
        if action == 'C':
            action = 'Created'
        elif action == 'U':
            action = 'Updated'
        elif action == 'D':
            action = 'Deleted'

        return action

    def get_timestamp_formatted(self, date: datetime) -> str:
        return datetime.strftime(date, "%d-%m-%Y %H:%M:%S")

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'action': self.get_action_described(instance.action),
            'date': self.get_timestamp_formatted(instance.timestamp),
            'user_id': instance.user_id,
            'user_name': instance.username,
            'user_email': instance.user_email,
            'camera_id': instance.cam_id,
            'camera_ip': instance.cam_ip,
            'camera_port': instance.cam_port,
            'camera_file': instance.cam_file,
            'camera_username': instance.cam_username,
            'camera_password': instance.cam_password,
        }
        return data
