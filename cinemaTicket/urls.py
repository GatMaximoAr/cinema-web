from rest_framework import routers
from .viewSets import CinemaRoomViewSet

router = routers.DefaultRouter()

router.register("api/cinema-room", CinemaRoomViewSet, "room")

urlpatterns = router.urls
