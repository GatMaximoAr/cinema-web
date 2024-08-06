from rest_framework import routers
from .viewSets import CinemaRoomViewSet, ProjectionViewSet

router = routers.DefaultRouter()

router.register("api/cinema-room", CinemaRoomViewSet, "room")
router.register("api/projection", ProjectionViewSet, "projection")

urlpatterns = router.urls
