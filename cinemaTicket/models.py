from django.db import models
from datetime import date


class CinemaRoom(models.Model):
    name = models.CharField(max_length=20)
    capacity = models.SmallIntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    poster_image = models.ImageField(upload_to="posters/")

    def __str__(self):
        return self.name


class Projection(models.Model):
    projection_date = models.DateTimeField()
    cinema_rooms = models.ManyToManyField(CinemaRoom)
    created_at = models.DateField(default=date.today)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"projection_date: {self.projection_date}, \
        movie: {self.movie.name}"
