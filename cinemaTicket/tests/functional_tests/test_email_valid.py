import pytest
from cinemaTicket.models import ValidEmail
from django.core.exceptions import ObjectDoesNotExist
from django.core import mail
from cinemaTicket.utils import generate_otp
from django.utils import timezone

url = "/api/email/"


@pytest.mark.django_db
def test_can_create_email(api_client):
    # given an endpoint and database

    # when the user post some data in the end point 'api/email/'

    data = {"email": "testemail@gmail.com"}

    response = api_client.post(path=url, data=data, format="json")
    # then get the email-valid data
    response_data = response.data
    # print(response_data)

    assert response_data["email"] == data["email"]
    assert response_data["otp_expires_at"] != None


@pytest.mark.django_db
def test_can_reject_get_email(api_client):

    response = api_client.get(path=url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_can_reject_update_email(api_client_with_credentials):

    response = api_client_with_credentials.patch(
        path=url + "1/", data={"email": "test@email"}, format="json"
    )

    assert response.status_code == 405


@pytest.mark.django_db
def test_can_delete_email(api_client_with_credentials):

    response = api_client_with_credentials.delete(path=url + "1/")

    try:
        db_query = ValidEmail.objects.get(pk=1)
        pytest.fail(reason="the object exist!")

    except ObjectDoesNotExist:
        assert True


@pytest.mark.django_db
def test_can_send_mail_on_create(api_client):

    data = {"email": "testemail@gmail.com"}

    response = api_client.post(path=url, data=data, format="json")

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "verify email"


@pytest.mark.django_db
def test_can_verify_otp(api_client):

    data = {"email": "testemail@gmail.com"}

    request = api_client.post(path=url, data=data, format="json")

    db_query = ValidEmail.objects.filter(email=data["email"]).first()

    # print(request.data)

    response = api_client.post(
        path="/api/email-verify/", data={"otp_code": db_query.otp_code}, format="json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_can_reject_if_is_verified_email(api_client):

    expires_ = timezone.now() + timezone.timedelta(minutes=5)

    verified_email = ValidEmail(
        email="test@email.org",
        is_verified=True,
        otp_code=generate_otp(),
        otp_expires_at=expires_,
    )
    verified_email.save()

    response = api_client.post(
        path="/api/email-verify/",
        data={"otp_code": verified_email.otp_code},
        format="json",
    )

    assert response.status_code == 409


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [("/api/email-verify/"), ("api/refresh-otp/")],
    ids=["verified_email", "refresh_email"],
)
def test_can_raise_not_found(api_client, url):

    response = api_client.post(path=url, data={"otp_code": 123456}, format="json")

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [("email-verify/"), ("refresh-otp/")],
    ids=["verified_email", "refresh_email"],
)
def test_can_refuse_bad_request(api_client, url):

    response = api_client.post(
        path="/api/" + url, data={"some_bad_field": 123456}, format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_can_reject_if_is_otp_expired(api_client):

    expires_ = timezone.now() - timezone.timedelta(minutes=5)

    expired_otp = ValidEmail(
        email="test@email.org",
        is_verified=False,
        otp_code=generate_otp(),
        otp_expires_at=expires_,
    )
    expired_otp.save()

    response = api_client.post(
        path="/api/email-verify/",
        data={"otp_code": expired_otp.otp_code},
        format="json",
    )

    assert response.status_code == 410


@pytest.mark.django_db
def test_can_send_mail_on_refresh_otp(api_client, given_exiting_email):

    data = {"email": "testemail@gmail.com"}

    response = api_client.post(path="/api/refresh-otp/", data=data, format="json")

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "verify email"

    assert response.status_code == 200


@pytest.mark.django_db
def test_can_reject_if_is_verified_email_in_refresh(api_client):

    expires_ = timezone.now() + timezone.timedelta(minutes=5)

    verified_email = ValidEmail(
        email="test@email.org",
        is_verified=True,
        otp_code=generate_otp(),
        otp_expires_at=expires_,
    )
    verified_email.save()

    response = api_client.post(
        path="/api/refresh-otp/", data={"email": verified_email.email}, format="json"
    )

    assert response.status_code == 409
