from django.db import models


class IATAKorean(models.Model):
    """
    IATA 공항 코드를 한글로 풀어 쓴 버전
    """
    korean_name = models.CharField(max_length=20)

    def __str__(self):
        return self.korean_name


class IATACode(models.Model):
    """
    3글자로 축약된 IATA 공항 코드
    """
    korean_name = models.OneToOneField(
        IATAKorean,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    code_name = models.SlugField(max_length=3)

    def __str__(self):
        return f'{self.korean_name} ({self.code_name})'


class Transport(models.Model):
    """
    IATA 코드와 비행기 코드로 조합된 항공편 일정
    """
    flight_code = models.CharField(max_length=10)
    start_IATA = models.ForeignKey(
        IATACode,
        related_name='start_airport',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    end_IATA = models.ForeignKey(
        IATACode,
        related_name='end_airport',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    start_time = models.DateTimeField(
        blank=True,
        null=True,
    )
    end_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.flight_code
