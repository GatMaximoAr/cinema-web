import pytest

prefix = "/api/"

pytestmark = pytest.mark.parametrize(
    "url, data",
    [
        pytest.param(
            prefix + "cinema-room/",
            {"name": "B1", "capacity": 100},
            id="create_cinema_room",
        ),
    ],
)


@pytest.mark.django_db
def test_can_get_success_response(url, data, api_client_with_credentials):

    request = api_client_with_credentials.post(path=url, data=data, format="json")
    assert request.status_code == 201


@pytest.mark.django_db
def test_can_reject_malformed_request_body(url, data, api_client_with_credentials):

    dirty_data = {"bad_data": 2, "pikachu": "some description"}

    request = api_client_with_credentials.post(path=url, data=dirty_data, format="json")

    assert request.status_code == 400


@pytest.mark.django_db
def test_can_reject_unauthorized_request(url, data, api_client):

    request = api_client.post(path=url, data=data, format="json")

    assert request.status_code == 403
