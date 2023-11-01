from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.base.api import TotalListApiView
from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import (UserSerializer, UserListSerializer,
                                        UserHistoricalListSerializer,
                                        FaceCaptureSerializer)
from apps.users.models import User, UserActionLog


class UserViewSet(Authentication, ModelViewSet):
    # permissions_required = ('users.view_user', 'users.add_user', 'users.change_user', 'users.delete_user')
    response: Response = None

    def get_serializer_class(self):
        serializer_class = None
        if self.action == 'list':
            serializer_class = UserListSerializer
        # elif self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
        else:
            serializer_class = UserSerializer
        return serializer_class

    def get_queryset(self, pk=None):
        query = None
        if pk is None:
            if self.user.is_superuser :
                query = self.get_serializer().Meta.model.objects.filter(is_active=True,is_superuser=False)
            elif not self.user.is_superuser and self.user.is_staff:
                query = self.get_serializer().Meta.model.objects.filter(is_active=True,is_superuser=False,is_staff=False)
        else:
            query = self.get_serializer().Meta.model.objects.filter(id=pk, is_active=True).first()
        return query

    def list(self, request, *args, **kwargs):
        try:
            user_serializer = self.get_serializer(self.get_queryset(), many=True)
        except Exception as e:
            self.response = Response(f"error: {str(e)}", status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            if self.user.has_perm('users.view_user'):
                self.response = Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                self.response = Response(
                    {'error': 'No tienes el permiso para realizar esta acción.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return self.response

    def create(self, request, *args, **kwargs):
        if self.user.has_perm('users.add_user'):
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                # SAVE LOG OF RECENT USER ACTION
                _ = UserActionLog.objects.create(
                    user=self.user,
                    action='C',
                    target_user=user,
                    timestamp=timezone.now()
                )
                self.response = Response(
                    {'message': '¡Usuario creado correctamente!'},
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
        return self.response

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer_class = self.get_serializer_class()
        try:
            if self.user.has_perm('users.view_user'):
                if self.get_queryset(pk):
                    user_serializer = serializer_class(instance=self.get_queryset(pk))
                    if user_serializer:
                        self.response = Response(
                            user_serializer.data,
                            status=status.HTTP_200_OK)
                    else:
                        self.response = Response(
                            {'errors': user_serializer.errors},
                            status=status.HTTP_404_NOT_FOUND)
                else:
                    self.response = Response(
                            {'message': 'Usuario no encontrado.'},
                            status=status.HTTP_400_BAD_REQUEST)
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

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer_class = self.get_serializer_class()
        if self.user.has_perm('users.change_user'):
            # TODO: VERIFY THAT THE USER IS STAFF CAN'T ERASE OR UPDATE A SUPERUSER
            user_to_modify = self.get_queryset(pk)
            if user_to_modify:
                if (not self.user.is_superuser and self.user.is_staff) and (user_to_modify.is_superuser):
                    self.response = Response(
                        {'message': 'No tienes el permiso para modificar un administrador'},
                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_serializer = serializer_class(user_to_modify, data=request.data)
                    if user_serializer.is_valid():
                        user_serializer.save()
                        # SAVE LOG OF RECENT USER ACTION
                        _ = UserActionLog.objects.create(
                            user=self.user,
                            action='U',
                            target_user=self.get_queryset(pk),
                            timestamp=timezone.now()
                        )
                        self.response = Response(user_serializer.data, status=status.HTTP_200_OK)
                    else:
                        self.response = Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.response = Response({'message': 'Usuario no encontrado.'},
                                         status=status.HTTP_404_NOT_FOUND)
        else:
            self.response = Response(
                {'error': 'No tienes el permiso para realizar esta acción.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return self.response

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.user.has_perm('users.delete_user'):
            user = self.get_queryset().filter(id=pk).first()
            if user:
                if self.user.id == user.id:
                    self.response = Response(
                        {'error': 'No puedes eliminar tu propia cuenta.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                # elif self.user.is_superuser:
                #     user.delete()
                #     # user.is_active = False
                #     # user.save()
                #     self.response = Response({'message': 'Usuario eliminado correctamente!'}, status=status.HTTP_200_OK)
                elif (not self.user.is_superuser and self.user.is_staff) and (user.is_staff or user.is_superuser):
                    self.response = Response(
                        {'error': 'No tienes el permiso para eliminar un administrador.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                else:
                    # SAVE LOG OF RECENT USER ACTION
                    _ = UserActionLog.objects.create(
                        user=self.user,
                        action='D',
                        target_user=user,
                        timestamp=timezone.now()
                    )
                    # user.delete()
                    user.is_active = False
                    user.save()
                    self.response = Response({'message': 'Usuario eliminado correctamente!'}, status=status.HTTP_200_OK)
            else:
                self.response = Response({'message': 'No existe un usuario con esos datos'}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.response = Response(
                {'error': 'No tienes el permiso para realizar esta acción.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return self.response


class UserHistoricalAPIView(ListAPIView):
    serializer_class = UserHistoricalListSerializer

    def get_queryset(self):
        #model = self.get_serializer().Meta.model.objects.all().order_by('-timestamp')[:10]
        model = self.get_serializer().Meta.model.objects.all().order_by('-timestamp')
        return model

    def get(self, request, *args, **kwargs):
        historical_serializer = self.get_serializer(self.get_queryset(), many=True)
        try:
            # TODO: CHECK USER_HISTORICALUSER
            response = Response(historical_serializer.data,
                                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response(
                {'error': 'There is a problem with the query.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class TotalUsersView(TotalListApiView):
    serializer_class = UserListSerializer


class FaceCaptureCreateAPIView(CreateAPIView):
    serializer_class = FaceCaptureSerializer
    response = None

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        user = User.objects.filter(id=user, is_active=True).first()
        if user:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    self.response = Response(
                            {'error': 'Imagen creada correctamente.'},
                            status=status.HTTP_201_CREATED
                        )
                except Exception as e:
                    print(str(e))
                    self.response = Response(
                            {'error': 'Por favor contacta con servicio tecnico.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
            else:
                self.response = Response(
                    {'error': 'Revisa los datos enviados.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            self.response = Response(
                    {'error': 'El usuario no existe.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return self.response


class FaceCaptureListAPIView(ListAPIView):
    serializer_class = FaceCaptureSerializer
    response = None

    def get_queryset(self):
        query = self.serializer_class().Meta.model.objects.all()
        return query

    def list(self, request, *args, **kwargs):
        try:
            face_capture_serializer = self.get_serializer(self.get_queryset(),
                                                          many=True)
            self.response = Response(face_capture_serializer.data,
                                     status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            self.response = Response(
                    {'error': 'Por favor contacte al servicio técnico.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return self.response
