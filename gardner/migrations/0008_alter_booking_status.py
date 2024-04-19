# Generated by Django 5.0.3 on 2024-04-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardner', '0007_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('cancelled', 'Cancelled'), ('completed', 'Completed'), ('pending', 'Panding')], default='pending', max_length=10),
        ),
    ]