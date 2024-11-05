import pytest
import uuid
from rest_framework.test import APIClient
from cinemaTicket.models import *
from io import BytesIO
from PIL import Image
from django.utils import timezone
from cinemaTicket.utils import generate_otp
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission


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
    room2 = CinemaRoom(name="A1", capacity=1)
    room1.save()
    room2.save()


@pytest.fixture
def given_cinema_projection(db, given_cinema_rooms, given_cinema_movie):
    movie = Movie.objects.get(pk=1)
    given_room = CinemaRoom.objects.get(pk=1)
    projection = Projection(
        projection_date="2024-08-04:12:51", movie=movie, cinema_room=given_room
    )
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
def given_exiting_email():
    expires_ = timezone.now() - timezone.timedelta(minutes=5)
    test_email = ValidEmail(
        email="testemail@email.org",
        is_verified=True,
        otp_code=generate_otp(),
        otp_expires_at=expires_,
    )
    test_email.save()

    test_email1 = ValidEmail(
        email="test@email.org",
        is_verified=False,
        otp_code=generate_otp(),
        otp_expires_at=expires_,
    )
    test_email1.save()


@pytest.fixture
def given_existing_data(
    given_cinema_rooms,
    given_cinema_projection,
    given_cinema_movie,
    given_exiting_email,
):

    email = ValidEmail.objects.get(pk=1)

    projection = Projection.objects.get(pk=1)

    ticket = Ticket(customer_name="test customer", email=email, projection=projection)
    ticket.save()


@pytest.fixture
def given_sold_out_projection(
    given_cinema_movie, given_cinema_rooms, given_exiting_email
):

    email = ValidEmail.objects.get(pk=1)

    movie = Movie.objects.get(pk=1)
    given_room = CinemaRoom.objects.get(pk=2)
    projection = Projection(
        projection_date="2024-08-04:12:51", movie=movie, cinema_room=given_room
    )
    projection.save()

    ticket = Ticket(customer_name="test customer", email=email, projection=projection)
    ticket.save()


@pytest.fixture
def ticker_verifier(db, api_client):
    new_group = Group.objects.get_or_create(name='verified_ticket') 
    user = User.objects.create(username="jhon", password="some-strong-pass")
    user.save()
    user.groups.set(new_group)
    user.save()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
