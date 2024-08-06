from django.db import models
from datetime import date


class CinemaRoom(models.Model):
    name = models.CharField(max_length=20)
    capacity = models.SmallIntegerField()


class Projection(models.Model):
    projection_date = models.DateField()
    start_time = models.TimeField()
    cinema_rooms = models.ManyToManyField(CinemaRoom)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return f"projection_date: {self.projection_date}, \
        start_time: {self.start_time}, cinema_room: {self.cinema_rooms}, \
        created_at: {self.created_at}"
