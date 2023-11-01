from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from apps.base.api import TotalListApiView, BaseHistoricGroupByMonthListAPIView
from apps.cameras.models import Camera
from apps.clips.api.serializers import ClipSerializer, ClipListSerializer, ClipHistoricGroupByMonthSerializer
from apps.users.authentication_mixins import Authentication


class ClipViewSet(Authentication, ModelViewSet):
    # permission_required = ('cameras.view_camera', 'cameras.add_camera', 'cameras.change_camera', 'cameras.delete_camera')
    parser_classes = (MultiPartParser, FormParser)
    # serializer_class = ClipSerializer
    response = None

    def get_serializer_class(self):
        serializer_class = None
        if self.action == 'list':
            serializer_class = ClipListSerializer
        # elif self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
        else:
            serializer_class = ClipSerializer
        return serializer_class

    def get_queryset(self, pk=None):
        query = None
        if pk is None:
            query = self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            query = self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        return query

    def list(self, request, *args, **kwargs):
        try:
            clip_serializer = self.get_serializer(
                self.get_queryset(), many=True)
        except Exception as e:
            self.response = Response(
                {'message': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            if self.user.has_perm('clips.view_clip'):
                self.response = Response(
                    clip_serializer.data, status=status.HTTP_200_OK)
            else:
                self.response = Response(
                    {'error': 'No tienes el permiso para realizar esta acción.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return self.response

    # def perform_create(self, serializer):
    #     # calcula el tamaño del archivo en bytes
    #     file_size = serializer.validated_data['file'].size
    #     serializer.save(size=file_size)

    def create(self, request, *args, **kwargs):
        try:
            # TODO: MIGHT NOT NEED USER TOKEN AUTHENTICATION
            if self.user.has_perm('clips.add_clip'):
                camera = Camera.objects.filter(
                    id=request.data.get('camera'), state=True).first()
                if camera:
                    serializer_class = self.get_serializer_class()
                    serializer = serializer_class(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        self.response = Response(
                            {'message': '¡Clip creado correctamente!'},
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        self.response = Response(
                            {'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    self.response = Response(
                        {'message': 'Cámara no existe.'},
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
            print(self.user)
            print(self.user.get_user_permissions())
            print(self.user.get_all_permissions())
            if self.user.has_perm('clips.view_clip'):
                if self.get_queryset(pk):
                    clip_serializer = self.serializer_class(
                        instance=self.get_queryset(pk))
                    if clip_serializer:
                        self.response = Response(
                            clip_serializer.data,
                            status=status.HTTP_200_OK)
                    else:
                        self.response = Response(
                            {'errors': clip_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.response = Response(
                        {'message': 'Clip no encontrado'},
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
            if self.user.has_perm('clips.change_clip'):

                serializer_class = self.get_serializer_class()
                if self.get_queryset(pk):
                    clip_serializer = serializer_class(
                        self.get_queryset(pk), data=request.data)
                    if clip_serializer.is_valid():
                        clip_serializer.save()
                        self.response = Response(
                            clip_serializer.data, status=status.HTTP_200_OK)
                    else:
                        self.response = Response(
                            clip_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.response = Response(
                        {'message': 'Clip no existe'}, status=status.HTTP_404_NOT_FOUND)
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
        if self.user.has_perm('cameras.delete_clip'):
            pk = kwargs.get('pk')
            camera = self.get_queryset().filter(id=pk).first()
            if camera:
                # camera.state = False
                # camera.save()
                camera.delete()
                self.response = Response(
                    {'message': '¡Clip eliminado correctamente!'}, status=status.HTTP_200_OK)
            else:
                self.response = Response(
                    {'message': 'No existe una cámara con esos datos.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.response = Response(
                {'error': 'No tienes el permiso para realizar esta acción.'},
                status=status.HTTP_403_FORBIDDEN)
        return self.response


class ClipHistoricGroupByMonthListView(BaseHistoricGroupByMonthListAPIView):
    serializer_class = ClipHistoricGroupByMonthSerializer


class TotalClipsView(TotalListApiView):
    serializer_class = ClipSerializer


class ClipsCreateAPIView(CreateAPIView):
    serializer_class = ClipSerializer

    def create(self, request, *args, **kwargs):
        try:
            camera_id = request.data.get('camera')
            camera = Camera.objects.filter(
                id=camera_id, state=True).first()
            if camera:
                camera_serializer = self.get_serializer_class()
                serializer = camera_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response = Response(
                        {'message': '¡Clip creado correctamente!'},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    response = Response(
                        {'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                response = Response(
                    {'message': 'Cámara no existe.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            response = Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response


class ClipsListAPIView(ListAPIView):
    serializer_class = ClipListSerializer

    def get_queryset(self):
        query = self.get_serializer().Meta.model.objects.filter(state=True)
        return query

    def list(self, request, *args, **kwargs):
        try:
            clip_serializer = self.get_serializer(
                self.get_queryset(), many=True)
        except Exception as e:
            response = Response(
                {'message': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        else:
            response = Response(clip_serializer.data,
                                status=status.HTTP_200_OK)

        return response


class ClipRetrieveAPIView(RetrieveAPIView):
    serializer_class = ClipListSerializer

    def get_queryset(self, pk=None):
        query = self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        return query

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        clip = self.get_queryset(pk)
        try:
            if clip:
                clip_serializer = self.serializer_class(instance=clip)
                if clip_serializer:
                    response = Response(
                        clip_serializer.data,
                        status=status.HTTP_200_OK)
                else:
                    response = Response(
                        {'errors': clip_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response(
                    {'message': 'Clip no encontrado'},
                    status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
