# Generated by Django 2.0.3 on 2018-03-26 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IATAKorean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('korean_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=10)),
                ('start_time', models.DateField(blank=True, null=True)),
                ('end_time', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IATACode',
            fields=[
                ('korean_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='flight.IATAKorean')),
                ('code_name', models.SlugField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='transport',
            name='end_IATA',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='end_airport', to='flight.IATACode'),
        ),
        migrations.AddField(
            model_name='transport',
            name='start_IATA',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='start_airport', to='flight.IATACode'),
        ),
    ]
