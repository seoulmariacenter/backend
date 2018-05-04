from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from . import apis

app_name = 'member'

urlpatterns = [
    path('sign-in/', apis.SignIn.as_view(), name='sign_in'),
    path('refresh/', refresh_jwt_token),
]
