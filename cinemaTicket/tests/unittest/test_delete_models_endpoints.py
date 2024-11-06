import pytest

prefix = "/api/"

pytestmark = pytest.mark.parametrize(
    "url",
    [
        pytest.param(prefix + "cinema-room/", id="delete_cinema_room"),
        pytest.param(prefix + "projection/", id="delete_projection"),
        pytest.param(prefix + "movie/", id="delete_movie"),
        pytest.param(prefix + "ticket/", id="delete_ticket"),
        pytest.param(prefix + "email/", id="delete_email"),
    ],
)


@pytest.mark.django_db
def test_can_get_success_response(
    url, api_client_with_credentials, given_existing_data
):

    request = api_client_with_credentials.delete(path=url + "1/")
    assert request.status_code == 204


@pytest.mark.django_db
def test_can_not_found_record(url, api_client_with_credentials, given_existing_data):

    request = api_client_with_credentials.delete(path=url + "100/")

    assert request.status_code == 404


@pytest.mark.django_db
def test_can_reject_unauthorized_request(url, api_client, given_existing_data):

    request = api_client.delete(path=url + "1/")

    assert request.status_code == 403
