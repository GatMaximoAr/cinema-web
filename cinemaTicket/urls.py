from rest_framework import routers
from .viewSets import *

router = routers.DefaultRouter()

router.register("api/cinema-room", CinemaRoomViewSet, "room")
router.register("api/projection", ProjectionViewSet, "projection")
router.register("api/movie", MovieViewSet, "movie")
router.register("api/ticket", TicketViewSet, "ticket")

urlpatterns = router.urls
