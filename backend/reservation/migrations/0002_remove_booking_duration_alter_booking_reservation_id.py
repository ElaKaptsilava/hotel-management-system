# Generated by Django 4.2.7 on 2023-12-05 14:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("reservation", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="duration",
        ),
        migrations.AlterField(
            model_name="booking",
            name="reservation_id",
            field=models.CharField(
                default=uuid.UUID("d8168f96-8126-4075-aaa0-d67a80060e19"),
                max_length=250,
            ),
        ),
    ]
