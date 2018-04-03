from django.urls import path

from . import apis

app_name = 'member'

urlpatterns = [
    path('sign-in/', apis.SignIn.as_view(), name='sign_in'),
]
