# Generated by Django 5.0 on 2023-12-07 14:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("discounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="discount",
            old_name="room",
            new_name="rooms",
        ),
    ]
