# Generated by Django 5.0.7 on 2024-07-20 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='bus_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]
