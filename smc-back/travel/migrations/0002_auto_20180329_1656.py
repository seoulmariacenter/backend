# Generated by Django 2.0.3 on 2018-03-29 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-start_time']},
        ),
    ]
