import logging

logger = logging.getLogger("apps")

from datetime import datetime

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tzlocal import get_localzone

# from rest_framework.authentication import TokenAuthentication
from .authentication import CustomTokenAuthentication as TokenAuthentication
from .models import User, UserDevice
from .models import UserToken as Token
from .serializers import LoginSerializer, SignUpSerializer, UserSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data            
            # Create user
            user = User.objects.create(
                email=data.get('email'),
                password=data.get('password'),
                name=data.get('name'),
                device_id=data.get('device_id'),
            )
            # Create user device info
            UserDevice.objects.create(
                user=user,
                device_id=data.get('device_id'),
                device_os=data.get('device_os'),
                device_os_version=data.get('device_os_version'),
            )
            return Response({'created': True}, status=status.HTTP_201_CREATED)

        return Response(
            {
                'created': False,
                'message': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Create or replace device info
            device, _ = UserDevice.objects.update_or_create(
                user=user,
                device_id=request.data['device_id'],
            )
            # Create or replace token by user, device
            token, _ = Token.get_or_create(user=user, device=device)
            user.token = token.key
            if user.time_zone:
                local_tz = get_localzone(user.time_zone)
                user.last_login = datetime.now(local_tz)
            else:
                user.last_login = datetime.now(get_localzone())
            
            user.save()
            return Response(
                {'status': True, 'token': token.key}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        token = request.auth
        if token is not None:
            try:
                user = UserSerializer(token.user).data                
                if user.get("token") != token.key:
                    logger.debug(f"User(email: {user.get('email')}, id: {user.get('id')}) token changed: {token.key} -> {user.get('token')}")
                    user.update(token=None)
                    token.delete()
                    return Response({'status': False, 'device_changed': True, 'message': '로그인 기기가 변경 되었습니다.\n다시 로그인 해주세요.'}, status=status.HTTP_401_UNAUTHORIZED)
                
                return Response({'status': True, 'user': user}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'status': False, 'message': '유효한 토큰이 아닙니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response({'status': False}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.auth
        user = User.objects.get(token=token)
        user.token = None
        user.save()
        token.delete()
        return Response({'status': True,}, status=status.HTTP_200_OK)