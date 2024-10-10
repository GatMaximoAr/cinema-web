import pytest

prefix = "/api/"

pytestmark = pytest.mark.parametrize(
    "url, data",
    [
        pytest.param(
            prefix + "ticket/",
            {
                "customer_name": "test customer",
                "email": "testemail@email.org",
                "projection": 1,
            },
            id="ticket",
        ),
        pytest.param(prefix + "email/", {"email": "test1@email.org"}, id="email"),
    ],
)


@pytest.mark.django_db
def test_can_get_success_response_on_unauthorized(
    api_client, url, data, given_existing_data
):

    request = api_client.post(path=url, data=data, format="json")
    assert request.status_code == 201


@pytest.mark.django_db
def test_can_reject_malformed_request_body(
    api_client_with_credentials, url, data, given_existing_data
):

    dirty_data = {"bad_data": 2, "pikachu": "some description"}

    request = api_client_with_credentials.post(path=url, data=dirty_data, format="json")

    assert request.status_code == 400


@pytest.mark.django_db
def test_can_reject_get(api_client, url, data, given_existing_data):

    request = api_client.get(path=url)
    assert request.status_code == 403


@pytest.mark.django_db
def test_can_reject_get_record_by_id(api_client, url, data, given_existing_data):

    request = api_client.get(path=url + "1/")
    assert request.status_code == 403
