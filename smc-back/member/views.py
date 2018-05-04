from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>서울마리아센터 API 서버</h1>')
