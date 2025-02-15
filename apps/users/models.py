from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now, timedelta


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, default=None)
    email = models.EmailField(unique=True, null=False, default=None)
    device_id = models.CharField(unique=True, null=False, default=None)
    time_zone = models.CharField(null=True, default=None)
    token = models.CharField(null=True, default=None)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    class Meta:
        db_table = 'user'
        ordering = ['-created_at']

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField()
    device_os = models.CharField()
    device_os_version = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_device'
        ordering = ['-created_at']

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    device_id = models.ForeignKey(UserDevice, on_delete=models.CASCADE, related_name='tokens')
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_token'
        ordering = ['-created_at']

    @staticmethod
    def get_expiry():
        return now() + timedelta(days=7)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.get_expiry()
        super().save(*args, **kwargs)
    
    def has_expired(self):
        return self.expires_at < now()
    
    @classmethod
    def get_or_create(cls, user, device):
        import hashlib
        user_data = f"{user.email}{user.id}{device.device_id}"
        key = hashlib.sha1(user_data.encode('utf-8')).hexdigest()[:40]
        token, created = cls.objects.get_or_create(
            user=user,
            device_id=device,
            defaults={
                'key': key,
                'expires_at': cls.get_expiry(),
            }
        )
        # Create new token if the token is expired
        if not created and token.has_expired():
            token.expires_at = cls.get_expiry()
            token.key = hashlib.sha1(f"{user_data}{now()}".encode('utf-8')).hexdigest()[:40]
            token.save()
            
        return token, created