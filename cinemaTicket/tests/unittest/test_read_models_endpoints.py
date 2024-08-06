import pytest

prefix = "/api/"

pytestmark = pytest.mark.parametrize(
    "url",
    [
        pytest.param(prefix + "cinema-room/", id="read_cinema_rooms"),
        pytest.param(prefix + "projection/", id="read_projection"),
    ],
)


@pytest.mark.django_db
def test_can_get_success_response(url, api_client, given_cinema_projection):

    request = api_client.get(path=url)
    assert request.status_code == 200


@pytest.mark.django_db
def test_can_reject_get_record_by_id(url, api_client, given_cinema_projection):

    request = api_client.get(path=url + "1/")
    assert request.status_code == 403
