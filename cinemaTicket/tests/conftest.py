import pytest
import uuid
from rest_framework.test import APIClient
from cinemaTicket.models import *
from io import BytesIO
from PIL import Image
from django.core.files.base import File


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def given_cinema_rooms(db):
    room1 = CinemaRoom(name="B1", capacity=100)
    room2 = CinemaRoom(name="A1", capacity=100)
    room1.save()
    room2.save()


@pytest.fixture
def given_cinema_projection(db, given_cinema_rooms, given_cinema_movie):
    movie = Movie.objects.get(pk=1)
    projection = Projection(projection_date="2024-08-04:12:51", movie=movie)
    projection.save()

    given_room = CinemaRoom.objects.get(pk=1)
    projection.cinema_rooms.add(given_room)
    projection.save()


@pytest.fixture
def test_image():
    file_obj = BytesIO()
    image = Image.new("RGB", size=(50, 50), color=(256, 0, 0))
    image.save(file_obj, "png")
    file_obj.name = "test_image.png"
    file_obj.seek(0)
    return file_obj


@pytest.fixture
def given_cinema_movie(test_image):

    movie = Movie(name="deadpool & wolverine", description="some description")
    movie.save()


@pytest.fixture
def given_existing_data(
    given_cinema_rooms, given_cinema_projection, given_cinema_movie
):
    projection = Projection.objects.get(pk=1)

    ticket = Ticket(
        customer_name="test customer", email="test@email.com", projection=projection
    )
    ticket.save()
