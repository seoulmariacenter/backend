# Generated by Django 2.0.3 on 2018-04-23 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20180422_2119'),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('gender', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservationhost',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='travel.Product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservationmember',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.ReservationHost'),
        ),
    ]