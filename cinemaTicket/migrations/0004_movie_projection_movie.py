# Generated by Django 5.0.7 on 2024-08-12 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinemaTicket", "0003_rename_cinema_room_projection_cinema_rooms"),
    ]

    operations = [
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
        migrations.AddField(
            model_name="projection",
            name="movie",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cinemaTicket.movie",
            ),
        ),
    ]