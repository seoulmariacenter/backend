# Generated by Django 2.0.3 on 2018-05-02 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_remove_reservationhost_date_checked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservationhost',
            options={'ordering': ['-date_joined']},
        ),
        migrations.AlterModelOptions(
            name='reservationmember',
            options={'ordering': ['pk']},
        ),
        migrations.AddField(
            model_name='reservationmember',
            name='is_adult',
            field=models.BooleanField(default=True),
        ),
    ]
