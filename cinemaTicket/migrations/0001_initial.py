# Generated by Django 5.0.7 on 2024-08-27 13:51

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CinemaRoom",
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
                ("name", models.CharField(max_length=20)),
                ("capacity", models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
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
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("poster_image", models.ImageField(upload_to="posters/")),
            ],
        ),
        migrations.CreateModel(
            name="Projection",
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
                ("projection_date", models.DateTimeField()),
                ("created_at", models.DateField(default=datetime.date.today)),
                ("cinema_rooms", models.ManyToManyField(to="cinemaTicket.cinemaroom")),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cinemaTicket.movie",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
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
                ("customer_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("is_validated", models.BooleanField(default=False)),
                (
                    "projection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cinemaTicket.projection",
                    ),
                ),
            ],
        ),
    ]
