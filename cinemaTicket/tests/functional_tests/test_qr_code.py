import re
import pytest
from django.core import mail
from cinemaTicket.utils import send_email_template, generate_qr_code_base64


@pytest.mark.django_db
def test_email_contains_qr_base64_image():
    qr_code = generate_qr_code_base64("hello world")

    ctx = {"qr_code": qr_code}

    send_email_template(
        ctx=ctx,
        template="cinemaTicket/ticket_template.html",
        receivers=["test@email.org"],
        email_subject="ticket sended",
    )

    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    email.subject == "ticket sended", "subject incorrect"
    html_body = email.alternatives[0][0]

    # print(html_body)

    base64_regex = r'<img\s+[^>]*src="data:image\/[^;]+;base64,([^"]+)"'
    match = re.search(base64_regex, html_body)

    assert match is not None, "dont find base64 image in email"
