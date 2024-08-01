import pytest
import uuid
from rest_framework.test import APIClient
from cinemaTicket.models import CinemaRoom


@pytest.fixture
def test_password():
    return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(
   db, create_user, api_client
):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def given_cinema_rooms(db):
    room = CinemaRoom(name='B1', capacity=100)
    room.save()
