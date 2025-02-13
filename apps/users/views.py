from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


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