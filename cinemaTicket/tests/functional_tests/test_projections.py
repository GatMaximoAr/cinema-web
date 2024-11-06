import pytest
from cinemaTicket.models import Projection
from django.core.exceptions import ObjectDoesNotExist

url = "/api/projection/"


@pytest.mark.django_db
def test_can_create_projection(api_client_with_credentials, given_existing_data):
    # Given a authenticated user and existen cinema rooms in database

    # When make a post to the /api/projection/ endpoint when some valid data
    data = {
        "projection_date": "2024-07-21 16:30",
        "cinema_room": 1,
        "movie": 1,
    }
    response = api_client_with_credentials.post(path=url, data=data, format="json")

    response_data = response.data
    # print(response_data)

    # Then the success respond should return the posted data
    assert response_data["projection_date"] == data["projection_date"]


@pytest.mark.django_db
def test_can_get_projections(api_client_with_credentials, given_cinema_projection):
    response = api_client_with_credentials.get(path=url)

    response_data = response.data

    db_query = Projection.objects.get(pk=response_data[0]["id"])

    assert db_query.id == response_data[0]["id"]


@pytest.mark.django_db
def test_can_update_projection(api_client_with_credentials, given_existing_data):

    data = {
        "projection_date": "2024-08-04 12:51",
        "cinema_room": 1,
        "movie": 1,
    }
    response = api_client_with_credentials.put(
        path=url + "1/", data=data, format="json"
    )

    response_data = response.data

    assert response_data["projection_date"] == data["projection_date"]


@pytest.mark.django_db
def test_can_delete_projection(api_client_with_credentials, given_cinema_projection):
    response = api_client_with_credentials.delete(path=url + "1/")

    try:
        db_query = Projection.objects.get(pk=1)
        pytest.fail(reason="the object exist!")

    except ObjectDoesNotExist:
        assert True
