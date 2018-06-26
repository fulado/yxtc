# Generated by Django 2.0.6 on 2018-06-26 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj_van_app', '0005_vehicle_is_secure'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='d_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='discovery',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]