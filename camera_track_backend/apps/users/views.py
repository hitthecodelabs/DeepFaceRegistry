from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import UserTokenSerializer


# Create your views here.
class UserToken(Authentication, APIView):
    response: Response

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user=UserTokenSerializer().Meta.model.objects.filter(username=username).first()
            )
            self.response = Response({
                'token': user_token.key
            }, status=status.HTTP_200_OK)
        except:
            self.response = Response({
                'error': 'Credenciales enviadas incorrectas'
            }, status=status.HTTP_400_BAD_REQUEST)

        return self.response


class Login(ObtainAuthToken):
    response = Response(
        {'message': 'Problema en el servidor, contacta servicio especializado.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

    def post(self, request, *args, **kwargs):
        # Calls ObtainAuthToken serializer (username and password)
        login_serializer = self.serializer_class(data=request.data, context={'request': request})

        if login_serializer.is_valid():
            user = login_serializer.validated_data.get('user')
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(instance=user)
                if created:
                    self.response = Response(
                        {
                            'token': token.key,
                            'user': user_serializer.data,
                            'message': 'Inicio de Sesión Exitoso'
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    # CLOSE ALL OPEN SESSIONS
                    """
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    self.response = Response(
                        {
                            'token': token.key,
                            'user': user_serializer.data,
                            'message': 'Inicio de Sesión Exitoso'
                        },
                        status=status.HTTP_201_CREATED
                    )
                    """
                    token.delete()
                    self.response = Response(
                        {'message': "Ya se ha iniciado sesión con este usuario."},
                        status=status.HTTP_409_CONFLICT
                    )
            else:
                self.response = Response(
                    {'message': "Revisa tus credenciales"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            self.response = Response(
                {'message': "Hubo un error en la validación"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return self.response


class Logout(APIView):
    response = Response(
        {'message': 'Problema en el servidor, contacta servicio especializado.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

    def post(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key=token).first()
            print(token)
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones de usuario eliminadas.'
                token_message = 'Token eliminado.'
                self.response = Response({
                    'token_message': token_message,
                    'session_message': session_message
                },
                    status=status.HTTP_200_OK
                )
            else:
                self.response = Response({
                    'error': 'No se ha encontrado un usuario con estas credenciales.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            self.response = Response({
                'error': 'No se ha encontrado token en la petición.'
            },
                status=status.HTTP_409_CONFLICT
            )
        return self.response
