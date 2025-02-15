from django.utils.timezone import now
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import UserToken


class CustomTokenAuthentication(TokenAuthentication):
    model = UserToken 
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authorization header missing')

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'token':
            raise AuthenticationFailed('Authorization header must be in the format "Token <token>"')

        token_key = parts[1]

        try:
            token = self.model.objects.get(key=token_key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)
    
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        if token.has_expired():
            token.delete()
            raise AuthenticationFailed('Token has expired')
        
        return (token.user, token)