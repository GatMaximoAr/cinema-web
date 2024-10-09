import base64
from io import BytesIO
import secrets
from django.core.mail import send_mail
from django.template.loader import render_to_string
import qrcode


def generate_otp():
    return secrets.token_hex(3)


def send_email_template(ctx: dict, template: str, receivers: list, email_subject: str):

    convert_to_html_content = render_to_string(template_name=template, context=ctx)

    send_mail(
        subject=email_subject,
        message="",
        from_email="web@mail.org",
        recipient_list=receivers,
        html_message=convert_to_html_content,
        fail_silently=True,
    )


def generate_qr_code_base64(qr_content: str):

    qr = qrcode.make(qr_content)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return qr_image_base64
