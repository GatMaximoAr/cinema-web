from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ValidEmail
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .utils import generate_otp, send_email_template


@api_view(["POST"])
def validate_email(request):
    otp_code = request.data.get("otp_code")
    if not otp_code:
        return Response(
            {"detail": "OTP code is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        db_email = ValidEmail.objects.get(otp_code=otp_code)

        if db_email.is_verified:
            return Response(
                {"detail": "The email is already verified."},
                status=status.HTTP_409_CONFLICT,
            )

        if db_email.otp_expires_at > timezone.now():

            db_email.is_verified = True
            db_email.save()
            return Response(
                {"detail": "The email has been successfully verified!"},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"detail": "The OTP has expired, please request a new one."},
                status=status.HTTP_410_GONE,
            )

    except ObjectDoesNotExist:
        return Response(
            {"detail": "No email associated with this OTP code was found."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
def refresh_otp(request):
    email = request.data.get("email")
    if not email:
        return Response(
            {"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        db_email = ValidEmail.objects.get(email=email)

        if db_email.is_verified:
            return Response(
                {"detail": "The email is already verified."},
                status=status.HTTP_409_CONFLICT,
            )

        else:
            db_email.otp_code = generate_otp()
            db_email.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
            db_email.save()

            send_email_template(
                ctx={"otp_code": db_email.otp_code},
                template="cinemaTicket/validate-email.html",
                email_subject="Your One-Time Password for Validation",
                receivers=[db_email.email],
            )

            return Response(
                {"detail": "The otp was refresh and send to you email!"},
                status=status.HTTP_200_OK,
            )

    except ObjectDoesNotExist:
        return Response(
            {"detail": "No email associated with this OTP code was found."},
            status=status.HTTP_404_NOT_FOUND,
        )
