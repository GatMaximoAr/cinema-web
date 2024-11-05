import pytest
from cinemaTicket.models import Ticket
from django.core.exceptions import ObjectDoesNotExist
from django.core import mail
import re

url = "/api/ticket/"


@pytest.mark.django_db
def test_can_create_ticket(api_client, given_existing_data, given_exiting_email):
    # Given a user and existen cinema projections in database

    # When make a post to the /api/ticket/ endpoint when some valid data
    data = {
        "customer_name": "test customer",
        "email": "testemail@email.org",
        "projection": 1,
    }
    response = api_client.post(path=url, data=data, format="json")

    response_data = response.data
    # print(response_data)

    # Then the success respond should return the posted data
    assert response_data["customer_name"] == data["customer_name"]


@pytest.mark.django_db
def test_can_update_ticket(
    api_client_with_credentials, given_existing_data, given_exiting_email
):

    data = {
        "customer_name": "test customer update",
        "email": "testemail@email.org",
        "projection": 1,
    }
    response = api_client_with_credentials.put(
        path=url + "1/", data=data, format="json"
    )

    response_data = response.data
    # print(response.status_code)

    assert response.status_code == 405


@pytest.mark.django_db
def test_can_delete_ticket(api_client_with_credentials, given_cinema_projection):
    response = api_client_with_credentials.delete(path=url + "1/")

    try:
        db_query = Ticket.objects.get(pk=1)
        pytest.fail(reason="the object exist!")

    except ObjectDoesNotExist:
        assert True


@pytest.mark.django_db
def test_limit_available_tickets(
    api_client, given_sold_out_projection, given_exiting_email
):

    data = {
        "customer_name": "test customer",
        "email": "testemail@email.org",
        "projection": 1,
    }
    response = api_client.post(path=url, data=data, format="json")

    response_data = response.data
    # print(response_data)

    assert response.status_code == 400


def test_can_send_ticket_by_email_on_create(
    api_client, given_existing_data, given_exiting_email
):

    data = {
        "customer_name": "test customer",
        "email": "testemail@email.org",
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


def test_can_retrieve_ticket_on_validate_page(
    ticker_verifier, given_existing_data
):

    ticket = Ticket.objects.get(pk=1)
    # print(ticket)

    response = ticker_verifier.get(
        path=f"/api/ticket/validate/{ticket.validate_code}/"
    )

    assert response.status_code == 200


def test_can_not_found_ticket_on_validate_page(
    api_client, ticker_verifier, given_existing_data
):

    response = ticker_verifier.get(path="/api/ticket/validate/2211/")

    assert response.status_code == 404
