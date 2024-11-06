from django.db import models
from datetime import date
from cinemaTicket.utils import generate_otp


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
    cinema_room = models.ForeignKey(CinemaRoom, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(default=date.today)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"projection_date: {self.projection_date}, \
        movie: {self.movie.name}"


class ValidEmail(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"email: {self.email}, is verifeid: {self.is_verified}"


class Ticket(models.Model):
    customer_name = models.CharField(max_length=50)
    email = models.ForeignKey(ValidEmail, on_delete=models.CASCADE)
    projection = models.ForeignKey(Projection, on_delete=models.CASCADE)
    is_validated = models.BooleanField(default=False)
    validate_code = models.CharField(max_length=6, default=generate_otp())

    def __str__(self):
        return f"id: {self.pk}, \
            projection date: {self.projection.projection_date}, \
            movie: {self.projection.movie.name}"
