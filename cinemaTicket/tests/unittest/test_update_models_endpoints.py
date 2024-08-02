import pytest

prefix = "/api/"

pytestmark = pytest.mark.parametrize(
    "url, data",
    [
        pytest.param(
            prefix + "cinema-room/1/",
            {"name": "new name", "capacity": 120},
            id="update_cinema_room",
        ),
    ],
)


@pytest.mark.django_db
def test_can_get_success_response(
    url, api_client_with_credentials, data, given_cinema_rooms
):

    request = api_client_with_credentials.put(path=url, data=data, format="json")
    assert request.status_code == 200


@pytest.mark.django_db
def test_can_reject_malformed_request_body(
    url, data, api_client_with_credentials, given_cinema_rooms
):

    dirty_data = {"bad_data": 2, "pikachu": "some description"}

    request = api_client_with_credentials.put(path=url, data=dirty_data, format="json")

    assert request.status_code == 400


@pytest.mark.django_db
def test_can_reject_unauthorized_request(url, data, api_client, given_cinema_rooms):

    request = api_client.put(path=url, data=data, format="json")

    assert request.status_code == 403