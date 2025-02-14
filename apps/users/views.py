from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, UserSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'created': True}, status=status.HTTP_201_CREATED)

        return Response(
            {
                'created': False,
                'message': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data
            user = Token.objects.get(key=token).user
            user_data = UserSerializer(user).data
            return Response(
                {'status': True, 'token': token, 'user': user_data}, status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        token = request.auth
        if token is not None:
            try:
                user = Token.objects.get(key=token).user
                user_data = UserSerializer(user).data
                return Response({'status': True, 'user': user_data}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'status': False, 'message': '유효한 토큰이 아닙니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response({'status': True}, status=status.HTTP_200_OK)
    

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