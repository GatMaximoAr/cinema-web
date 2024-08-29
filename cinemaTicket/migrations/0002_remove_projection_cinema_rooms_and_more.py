# Generated by Django 5.0.7 on 2024-08-29 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinemaTicket", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projection",
            name="cinema_rooms",
        ),
        migrations.AddField(
            model_name="projection",
            name="cinema_room",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cinemaTicket.cinemaroom",
            ),
        ),
    ]