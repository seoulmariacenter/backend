from django.db import models

from flight.models import Transport


class Product(models.Model):
    """
    하루 일정이 모여 만들어진 순례 상품
    """
    title = models.CharField(max_length=100)
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.CharField(max_length=10)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return self.title


class Date(models.Model):
    """
    스케줄이 모여 만들어진 하루 일정
    """
    date_num = models.PositiveSmallIntegerField()
    date_time = models.DateField()
    product = models.ForeignKey(
        Product,
        related_name='dates',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('product', 'date_time')
        ordering = ['date_time']

    def __str__(self):
        return f'제 {self.date_num}일'


class Schedule(models.Model):
    """
    하루 일정 안에 담긴 하나의 스케줄
    """
    place = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.ForeignKey(
        Date,
        on_delete=models.CASCADE,
    )
    transport = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.place
