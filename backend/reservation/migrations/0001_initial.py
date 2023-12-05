# Generated by Django 4.2.7 on 2023-12-05 14:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hotel_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "reservation_id",
                    models.CharField(
                        default=uuid.UUID("2eaaeea3-68c0-4099-88a1-85e6fa02f176"),
                        max_length=250,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Occupied", "Occupied"),
                            ("Canceled", "Canceled"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("duration", models.DurationField()),
                ("check_in", models.DateField(auto_now=True)),
                ("check_out", models.DateField(auto_now=True)),
                (
                    "rooms",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hotel_management.room",
                    ),
                ),
            ],
        ),
    ]
