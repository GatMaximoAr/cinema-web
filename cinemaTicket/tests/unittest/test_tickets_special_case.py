import pytest

url = "/api/ticket/"


@pytest.mark.django_db
def test_can_get_success_response_on_unauthorized(api_client, given_existing_data):

    data = {
        "customer_name": "test customer",
        "email": "test@email.com",
        "projection": 1,
    }

    request = api_client.post(path=url, data=data, format="json")
    assert request.status_code == 201


@pytest.mark.django_db
def test_can_reject_malformed_request_body(
    api_client_with_credentials, given_existing_data
):

    dirty_data = {"bad_data": 2, "pikachu": "some description"}

    request = api_client_with_credentials.post(path=url, data=dirty_data, format="json")

    assert request.status_code == 400


@pytest.mark.django_db
def test_can_get_success_response(api_client, given_cinema_projection):

    request = api_client.get(path=url)
    assert request.status_code == 403


@pytest.mark.django_db
def test_can_reject_get_record_by_id(api_client, given_cinema_projection):

    request = api_client.get(path=url + "1/")
    assert request.status_code == 403
