from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.compat import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SignIn(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            data = {
                'username': user.username,
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': '로그인 정보가 잘못되었습니다. 다시 시도해 주세요.'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
