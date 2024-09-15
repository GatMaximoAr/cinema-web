from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from cinemaTicket.models import *
from .serializers import *
from django.utils import timezone
import secrets
from django.core.mail import send_mail


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

    def get_permissions(self):
        """
        Setter the permissions of specific request action.
        """
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


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
        # Clona los datos de la solicitud original
        data = request.data.copy()

        # Modifica los datos según sea necesario
        data["otp_expires_at"] = timezone.now() + timezone.timedelta(
            minutes=5
        )  # Ejemplo de un campo adicional
        data["otp_code"] = secrets.token_hex(3)
        # print("otp code: " + data['otp_code'])

        # Instancia el serializer con los datos modificados
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Si la validación es exitosa, guarda el objeto
        self.perform_create(serializer)

        send_mail(
            "verify email",
            f"Here is the otp: {data["otp_code"]}.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        # Prepara la respuesta con los datos del objeto creado
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
