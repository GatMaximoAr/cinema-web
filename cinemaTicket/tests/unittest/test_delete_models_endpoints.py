import pytest

prefix = "/api/"

pytestmark = pytest.mark.parametrize(
    "url",
    [
        pytest.param(prefix + "cinema-room/1/", id="delete_cinema_room"),
        pytest.param(prefix + "projection/1/", id="delete_projection"),
    ],
)


@pytest.mark.django_db
def test_can_get_success_response(
    url, api_client_with_credentials, given_cinema_projection
):

    request = api_client_with_credentials.delete(path=url)
    assert request.status_code == 204


@pytest.mark.django_db
def test_can_not_found_record(
    url, api_client_with_credentials, given_cinema_projection
):

    request = api_client_with_credentials.delete(path="/api/cinema-room/201/")

    assert request.status_code == 404


@pytest.mark.django_db
def test_can_reject_unauthorized_request(url, api_client, given_cinema_projection):

    request = api_client.delete(path=url)

    assert request.status_code == 403
