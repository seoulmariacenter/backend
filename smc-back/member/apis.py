import json

from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SignIn(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        """
        로그인 뷰
        """
        # request.data로 authenticate
        user = authenticate(
            username=request.data.get('username', ''),
            password=request.data.get('password', ''),
        )

        # user가 확인되면 JWT token 생성
        if user:
            auth_payload = jwt_payload_handler(user)
            token = jwt_encode_handler(auth_payload)

            data = {'token': token}

            return HttpResponse(
                json.dumps(data),
                content_type='application/json; charset=utf-8',
                status=status.HTTP_200_OK
            )

        # user가 확인되지 않으면 오류 발생
        else:
            return Response(
                {'message': '아이디/패스워드가 올바르지 않습니다'},
                status=status.HTTP_400_BAD_REQUEST)
