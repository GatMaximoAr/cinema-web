import pytest
from cinemaTicket.models import Ticket
from django.core.exceptions import ObjectDoesNotExist
from django.core import mail
import re

url = "/api/ticket/"


@pytest.mark.django_db
def test_can_create_ticket(api_client, given_existing_data):
    # Given a user and existen cinema projections in database

    # When make a post to the /api/ticket/ endpoint when some valid data
    data = {
        "customer_name": "test customer",
        "email": "test@email.com",
        "projection": 1,
    }
    response = api_client.post(path=url, data=data, format="json")

    response_data = response.data
    # print(response_data)

    # Then the success respond should return the posted data
    assert response_data["customer_name"] == data["customer_name"]


@pytest.mark.django_db
def test_can_get_ticket(api_client_with_credentials, given_existing_data):
    response = api_client_with_credentials.get(path=url)

    response_data = response.data

    db_query = Ticket.objects.get(pk=response_data[0]["id"])

    assert db_query.id == response_data[0]["id"]


@pytest.mark.django_db
def test_can_update_ticket(api_client_with_credentials, given_existing_data):

    data = {
        "customer_name": "test customer update",
        "email": "test@email.com",
        "projection": 1,
    }
    response = api_client_with_credentials.put(
        path=url + "1/", data=data, format="json"
    )

    response_data = response.data

    assert response_data["customer_name"] == data["customer_name"]


@pytest.mark.django_db
def test_can_delete_ticket(api_client_with_credentials, given_cinema_projection):
    response = api_client_with_credentials.delete(path=url + "1/")

    try:
        db_query = Ticket.objects.get(pk=1)
        pytest.fail(reason="the object exist!")

    except ObjectDoesNotExist:
        assert True


@pytest.mark.django_db
def test_limit_available_tickets(api_client, given_sold_out_projection):

    data = {
        "customer_name": "test customer",
        "email": "test@email.com",
        "projection": 1,
    }
    response = api_client.post(path=url, data=data, format="json")

    response_data = response.data
    # print(response_data)

    assert response.status_code == 400


def test_can_send_ticket_by_email_on_create(api_client, given_existing_data):

    data = {
        "customer_name": "test customer",
        "email": "test@email.com",
        "projection": 1,
    }
    api_client.post(path=url, data=data, format="json")

    assert len(mail.outbox) == 1, "no emails in outbox"

    email = mail.outbox[0]
    email.subject == "ticket sended", "subject incorrect"
    html_body = email.alternatives[0][0]

    # print(html_body)

    base64_regex = r'<img\s+[^>]*src="data:image\/[^;]+;base64,([^"]+)"'
    match = re.search(base64_regex, html_body)

    assert match is not None, "dont find base64 image in email"
