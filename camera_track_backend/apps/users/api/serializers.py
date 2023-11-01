from datetime import datetime

from django.contrib.auth.models import Permission
from rest_framework.serializers import ModelSerializer

from apps.users.models import User, UserActionLog, FaceCapture
from apps.users.utils import email_notification


class UserTokenSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'is_staff','is_superuser')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        try:
            validated_data.pop('is_superuser')
        except KeyError as e:
            print("Error:", e)
        validated_data['is_active'] = True if validated_data.get('is_active') is None else validated_data.get('is_active')
        print(validated_data)

        # user = User(**validated_data)
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            last_name=validated_data.get('last_name'),
            image=validated_data.get('image'),
            is_staff=validated_data.get('is_staff')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        # USER 29 ADD, 30 CHANGE, 31 DELETE, 32 VIEW
        # CAMERA 21 ADD, 22 CHANGE, 23 DELETE, 24 VIEW
        # CLIP 49 ADD, 50 CHANGE, 51 DELETE, 52 VIEW
        staff_perms = Permission.objects.filter(codename__in=['add_camera', 'change_camera', 'delete_camera', 'view_camera',
                                                'add_user', 'change_user', 'delete_user', 'view_user',
                                                'add_clip', 'change_clip', 'delete_clip', 'view_clip'])

        user_perms = Permission.objects.filter(codename__in=['view_camera', 'view_clip'])
        if user.is_staff:
            user.user_permissions.clear()
            # VIEW CAMERA PERMISSION
            # user.user_permissions.set([21, 22, 23, 24, 29, 30, 31, 32, 49, 50, 51, 52])
            user.user_permissions.set(staff_perms)
        elif not user.is_staff:
            user.user_permissions.clear()
            # VIEW CAMERA PERMISSION
            # user.user_permissions.add(24, 52)
            user.user_permissions.set(user_perms)
        user.save()
        receiver = list()
        receiver.append(user.email)

        try:
            email_notification(
               sjt='Usuario Camera Track',
               msg='Se ha creado su cuenta en la app Camera Track de forma satisfactoria.',
               address=receiver)
        except Exception as e:
            print('Error:', str(e))
        return user

    def update(self, instance, validated_data):
        updated_user: User = super().update(instance, validated_data)
        updated_user.set_password(validated_data.get('password'))
        updated_user.save()
        staff_perms = Permission.objects.filter(codename__in=['add_camera', 'change_camera', 'delete_camera', 'view_camera',
                                                'add_user', 'change_user', 'delete_user', 'view_user',
                                                'add_clip', 'change_clip', 'delete_clip', 'view_clip'])

        user_perms = Permission.objects.filter(codename__in=['view_camera', 'view_clip'])
        if updated_user.is_staff:
            updated_user.user_permissions.clear()
            # VIEW CAMERA PERMISSION
            updated_user.user_permissions.set(staff_perms)
        elif not updated_user.is_staff:
            updated_user.user_permissions.clear()
            # VIEW CAMERA PERMISSION
            updated_user.user_permissions.add(user_perms)
        updated_user.save()
        return updated_user


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'username': instance.username,
            'name': instance.name,
            'last_name': instance.last_name,
            'email': instance.email,
            'password': instance.password,
            'is_staff': instance.is_staff
        }
        return data


class UserHistoricalListSerializer(ModelSerializer):
    # target_user = UserListSerializer(read_only=True)
    # user = UserListSerializer(read_only=True)

    class Meta:
        model = UserActionLog
        # exclude = ['password', 'image']
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
            'user_affected': instance.target_user.id,
            'user_affected_name': instance.target_user.name,
            'user_affected_last_name': instance.target_user.last_name,
            'user_responsible': instance.user.id,
            'user_responsible_name': instance.user.name,
            'user_responsible_last_name': instance.user.last_name
        }
        return data


class FaceCaptureSerializer(ModelSerializer):

    class Meta:
        model = FaceCapture
        # exclude = ['password', 'image']
        fields = '__all__'
