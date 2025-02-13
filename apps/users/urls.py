from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
]
