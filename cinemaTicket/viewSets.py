from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *


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
