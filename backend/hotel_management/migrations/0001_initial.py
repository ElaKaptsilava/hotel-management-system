# Generated by Django 4.2.7 on 2023-12-05 12:45

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hotel",
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
                ("name", models.CharField(max_length=250)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("city", models.CharField(max_length=250)),
                ("country", models.CharField(max_length=250)),
                ("street", models.CharField(max_length=250)),
                ("state", models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="Room",
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
                ("room_number", models.IntegerField(unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Available", "Available"),
                            ("NotAvailable", "Not Available"),
                            ("Reserved", "Reserved"),
                            ("Occupied", "Occupied"),
                        ],
                        default="Available",
                        max_length=15,
                    ),
                ),
                ("prise_per_day", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                (
                    "hotel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hotel_management.hotel",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="hotel",
            name="location",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="hotel_management.location",
            ),
        ),
    ]
