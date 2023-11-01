# from django.db.models.functions import TruncMonth
# from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
# from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from apps.base.api import TotalListApiView, BaseHistoricGroupByMonthListAPIView
from apps.users.authentication_mixins import Authentication
from apps.cameras.models import Camera, CameraActionLog
from apps.users.models import User
from apps.cameras.api.serializers import (CameraSerializer,
                                          CameraHistoricGroupByMonthSerializer,
                                          CameraHistoricSerializer)

from apps.cameras.utils import video_feed, stream_recognition, save_recognition_person


class CameraViewSet(Authentication, ModelViewSet):
    # permission_required = ('cameras.view_camera', 'cameras.add_camera', 'cameras.change_camera', 'cameras.delete_camera')
    serializer_class = CameraSerializer
    response = None

    def get_queryset(self, pk=None):
        query = None
        if pk is None:
            query = self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            query = self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        return query

    def list(self, request, *args, **kwargs):
        try:
            camera_serializer = self.get_serializer(
                self.get_queryset(), many=True)
        except Exception as e:
            self.response = Response(
                {'message': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            if self.user.has_perm('cameras.view_camera'):
                self.response = Response(
                    camera_serializer.data, status=status.HTTP_200_OK)
            else:
                self.response = Response(
                    {'error': 'No tienes el permiso para realizar esta acción.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return self.response

    def create(self, request, *args, **kwargs):
        try:
            camera = self.get_serializer().Meta.model.objects.filter(
                ip=request.data.get('ip'), state=True).first()
            if camera:
                self.response = Response(
                    {'message': 'Existe una cámara con esa ip, por favor revisa tu configuración.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if self.user.has_perm('cameras.add_camera'):
                    serializer = self.serializer_class(data=request.data)
                    if serializer.is_valid():
                        print(self.user.id, self.user.username, self.user.email)
                        camera = serializer.save()
                        print(camera)
                        # SAVE LOG OF RECENT USER ACTION
                        try:
                            CameraActionLog.objects.create(
                                user_id=self.user.id,
                                username=self.user.username,
                                user_email=self.user.email,
                                action='C',
                                cam_id=camera.id,
                                cam_ip=camera.ip,
                                cam_name=camera.name,
                                cam_port=camera.port,
                                cam_file=camera.file,
                                cam_username=camera.cam_username,
                                cam_password=camera.cam_password,
                                timestamp=timezone.now()
                            )
                        except Exception as e:
                            print(str(e))
                        # print(_)
                        self.response = Response(
                            {'message': '¡Cámara creada correctamente!'},
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        self.response = Response(
                            {'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    self.response = Response(
                        {'error': 'No tienes el permiso para realizar esta acción.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        except Exception as e:
            self.response = Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return self.response

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            if self.user.has_perm('cameras.view_camera'):
                if self.get_queryset(pk):
                    camera_serializer = self.serializer_class(
                        instance=self.get_queryset(pk))
                    if camera_serializer:
                        self.response = Response(
                            camera_serializer.data,
                            status=status.HTTP_200_OK)
                    else:
                        self.response = Response(
                            {'errors': camera_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.response = Response(
                        {'message': 'Cámara no encontrada'},
                        status=status.HTTP_404_NOT_FOUND)
            else:
                self.response = Response(
                    {'error': 'No tienes el permiso para realizar esta acción.'},
                    status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            self.response = Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return self.response

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            if self.user.has_perm('cameras.change_camera'):
                # camera = self.get_serializer().Meta.model.objects.filter(ip=request.data.get('ip'), state=True).first()
                # if camera:
                #     self.response = Response(
                #         {'message': 'Existe una cámara con esa ip, por favor revisa tu configuración.'},
                #         status=status.HTTP_400_BAD_REQUEST
                #     )
                # else:
                serializer_class = self.get_serializer_class()
                camera = self.get_queryset(pk)
                if camera:
                    cam_id = camera.id,
                    cam_ip = camera.ip,
                    cam_name = camera.name
                    cam_port = camera.port
                    cam_file = camera.file
                    cam_username = camera.cam_username
                    cam_password = camera.cam_password
                    camera_serializer = serializer_class(
                        camera, data=request.data)
                    if camera_serializer.is_valid():
                        camera_serializer.save()
                        # SAVE LOG OF RECENT USER ACTION
                        try:
                            CameraActionLog.objects.create(
                                user_id=self.user.id,
                                username=self.user.username,
                                user_email=self.user.email,
                                action='U',
                                cam_id=cam_id[0],
                                cam_ip=cam_ip[0],
                                cam_name=cam_name,
                                cam_port=cam_port,
                                cam_file=cam_file,
                                cam_username=cam_username,
                                cam_password=cam_password,
                                timestamp=timezone.now()
                            )
                        except Exception as e:
                            print(str(e))
                        self.response = Response(
                            camera_serializer.data, status=status.HTTP_200_OK)
                    else:
                        self.response = Response(
                            camera_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.response = Response(
                        {'message': 'Cámara no existe'}, status=status.HTTP_404_NOT_FOUND)
            else:
                self.response = Response(
                    {'error': 'No tienes el permiso para realizar esta acción.'},
                    status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            self.response = Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return self.response

    def destroy(self, request, *args, **kwargs):
        if self.user.has_perm('cameras.delete_camera'):
            pk = kwargs.get('pk')
            camera = self.get_queryset().filter(id=pk).first()
            if camera:
                cam_id = camera.id
                cam_ip = camera.ip
                cam_name = camera.name
                cam_port = camera.port
                cam_file = camera.file
                cam_username = camera.cam_username
                cam_password = camera.cam_password
                camera.delete()
                # SAVE LOG OF RECENT USER ACTION
                try:
                    CameraActionLog.objects.create(
                                user_id=self.user.id,
                                username=self.user.username,
                                user_email=self.user.email,
                                action='D',
                                cam_id=cam_id,
                                cam_ip=cam_ip,
                                cam_name=cam_name,
                                cam_port=cam_port,
                                cam_file=cam_file,
                                cam_username=cam_username,
                                cam_password=cam_password,
                                timestamp=timezone.now()
                        )
                except Exception as e:
                    print(str(e))
                self.response = Response(
                    {'message': '¡Cámara eliminada correctamente!'}, status=status.HTTP_200_OK)
            else:
                self.response = Response(
                    {'message': 'No existe una cámara con esos datos.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.response = Response(
                {'error': 'No tienes el permiso para realizar esta acción.'},
                status=status.HTTP_403_FORBIDDEN)
        return self.response


class CameraListAPIView(ListAPIView):
    serializer_class = CameraSerializer

    def get_queryset(self):
        query = self.get_serializer_class().Meta.model.objects.all()
        return query

    def get(self, request, *args, **kwargs):
        try:
            cameras = self.get_queryset()
            camera_serializer = self.get_serializer(cameras, many=True)
            response = Response(camera_serializer.data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            response = Response({'message': str(e)},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return response


class CameraHistoricGroupByMonthListView(BaseHistoricGroupByMonthListAPIView):
    serializer_class = CameraHistoricGroupByMonthSerializer


class TotalCamerasView(TotalListApiView):
    serializer_class = CameraSerializer


class VideoViewSet(GenericViewSet):
    serializer_class = CameraSerializer

    def get_queryset(self, pk: int):
        query = self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        return query

    @action(methods=['get'], detail=True)
    def show_video_stream(self, request, pk):
        camera: Camera = self.get_queryset(pk)
        users: User = User.objects.filter(is_active=True, is_superuser=False)
        if camera:
            response = video_feed(camera, users)
        else:
            response = Response(
                {'error': 'La cámara no existe.'},
                status=status.HTTP_400_BAD_REQUEST)
        # serializer = self.get_serializer_class()
        # data = serializer(video_feed()).data
        # return Response(video_feed(), status=status.HTTP_200_OK)

        return response
    
    @action(methods=['get'], detail=True)
    def show_video_stream_recognition(self, request):
        return stream_recognition()
    
    @action(methods=['post'], detail=True)
    def save_recognition_person(self, request):
        if request.method == 'POST':
            id_user = request.data.get('id_user')
            user = User.objects.filter(id=id_user, is_active=True).first()
            if user:
                save_recognition_person(id_user)
                response = Response(
                    {'message': '¡Reconocimiento guardado!'},
                    status=status.HTTP_201_CREATED
                )
            else:
                response = Response(
                    {'error': 'El usuario no existe.'},
                    status=status.HTTP_400_BAD_REQUEST)
            return response


class CameraHistoricChanges(ListAPIView):

    serializer_class = CameraHistoricSerializer

    def get_queryset(self):
        query = self.get_serializer().Meta.model.objects.all().order_by('-timestamp')[:10]
        return query

    def get(self, request, *args, **kwargs):
        historical_serializer = self.get_serializer(self.get_queryset(), many=True)
        try:
            # TODO: CHECK CAMERAS HISTORY
            response = Response(historical_serializer.data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response(
                {'error': 'There is a problem with the query.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
