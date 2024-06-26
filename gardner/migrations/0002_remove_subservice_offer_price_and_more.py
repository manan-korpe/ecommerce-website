# Generated by Django 5.0.3 on 2024-04-17 16:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subservice',
            name='offer_price',
        ),
        migrations.RemoveField(
            model_name='subservice',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='subservice',
            name='price',
        ),
        migrations.RemoveField(
            model_name='subservice',
            name='service_time',
        ),
        migrations.RemoveField(
            model_name='subservice',
            name='service_type',
        ),
        migrations.AddField(
            model_name='gardner',
            name='offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='gardner',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/img/GardnerService/'),
        ),
        migrations.AddField(
            model_name='gardner',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gardner',
            name='service_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gardner',
            name='service_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Panding'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=10),
        ),
    ]
