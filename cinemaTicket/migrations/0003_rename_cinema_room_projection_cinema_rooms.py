# Generated by Django 5.0.7 on 2024-08-03 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cinemaTicket", "0002_projection"),
    ]

    operations = [
        migrations.RenameField(
            model_name="projection",
            old_name="cinema_room",
            new_name="cinema_rooms",
        ),
    ]
