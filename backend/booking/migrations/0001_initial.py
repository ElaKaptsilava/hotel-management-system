# Generated by Django 4.2.7 on 2023-12-06 11:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                    "status",
                    models.CharField(
                        choices=[("Reserved", "Reserved"), ("Canceled", "Canceled")],
                        default="Reserved",
                        max_length=20,
                    ),
                ),
                ("check_in", models.DateField(default=django.utils.timezone.now)),
                ("check_out", models.DateField(default=django.utils.timezone.now)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hotel_management.room",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
