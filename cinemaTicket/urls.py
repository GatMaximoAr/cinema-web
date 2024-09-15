from rest_framework import routers
from django.urls import path
from . import views
from .api.viewSets import *

router = routers.DefaultRouter()

router.register("api/cinema-room", CinemaRoomViewSet, "room")
router.register("api/projection", ProjectionViewSet, "projection")
router.register("api/movie", MovieViewSet, "movie")
router.register("api/ticket", TicketViewSet, "ticket")
router.register("api/email", ValidEmailViewSet, "email")

urlpatterns = [
    path("api/email-verify/", views.validate_email),
    path("api/refresh-otp/", views.refresh_otp),
] + router.urls
