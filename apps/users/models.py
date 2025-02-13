# Create your models here.
from django.contrib.auth.hashers import make_password
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, default=None)
    email = models.EmailField(unique=True, null=False, default=None)
    password = models.CharField(max_length=255, null=False, default=None)
    time_zone = models.CharField(null=True, default=None)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']
    
    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False
    
    def set_password(self, password):
        self.password = make_password(password)
        
    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)