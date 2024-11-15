from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from cinemaTicket.models import *
from .serializers import *
from django.utils import timezone
from django.core.mail import send_mail
from cinemaTicket.utils import *
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import BasePermission

class verifiedTicket(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='verified_ticket').exists()



class CinemaRoomViewSet(viewsets.ModelViewSet):
    queryset = CinemaRoom.objects.all()
    serializer_class = CinemaRoomSerializer

    def get_permissions(self):
        """
        Setter the permissions of specific request action.
        """
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProjectionViewSet(viewsets.ModelViewSet):
    queryset = Projection.objects.all()
    serializer_class = ProjectionSerializer

    def get_permissions(self):
        """
        Setter the permissions of specific request action.
        """
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        """
        Setter the permissions of specific request action.
        """
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ["get", "post", "delete"]

    def get_permissions(self):
        """
        Setter the permissions of specific request action.
        """
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        elif self.action == "retrieve":
            permission_classes = [verifiedTicket]

        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        # print(serializer.data)

        qr_content = (
            f"localhost:8000/api/ticket/{str(serializer.data["validate_code"])}/"
        )
        # print(qr_content)
        qr_code = generate_qr_code_base64(qr_content)

        projection = Projection.objects.get(pk=serializer.data["projection"])

        ctx = {
            "qr_code": qr_code,
            "ticket": serializer.data,
            "movie": projection.movie.name,
            "projection": projection,
        }

        send_email_template(
            ctx=ctx,
            template="cinemaTicket/ticket-template.html",
            receivers=["test@email.org"],
            email_subject="ticket sended",
        )

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def retrieve(self, request, secret_key=None):

        if secret_key:
            ticket = get_object_or_404(Ticket, validate_code=secret_key)
            if ticket:
                expires = False
                if ticket.projection.projection_date < timezone.now():
                    expires = True
            print(expires)

            return render(
                request,
                "cinemaTicket/validate-ticket.html",
                {"ctx": ticket, "expires": expires},
            )


class ValidEmailViewSet(viewsets.ModelViewSet):
    queryset = ValidEmail.objects.all()
    serializer_class = ValidEmailSerializer
    http_method_names = ["get", "post", "delete"]

    def get_permissions(self):
        """
        Setter the permissions of specific request action.
        """
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data["otp_expires_at"] = timezone.now() + timezone.timedelta(minutes=5)
        data["otp_code"] = generate_otp()
        # print("otp code: " + data['otp_code'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        send_email_template(
            ctx={"otp_code": data["otp_code"]},
            template="cinemaTicket/validate-email.html",
            email_subject="Your One-Time Password for Validation",
            receivers=[serializer.data["email"]],
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
