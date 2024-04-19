# Generated by Django 5.0.3 on 2024-04-18 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardner', '0004_booking_gardner_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('pending', 'Panding'), ('cancelled', 'Cancelled')], default='pending', max_length=10),
        ),
    ]
