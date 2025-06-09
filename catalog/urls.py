from django.urls import include, path
from rest_framework.routers import DefaultRouter
from catalog.views import (
    PlayViewSet,
    ActorViewSet,
    GenreViewSet,
    PerformanceViewSet,
    TicketViewSet,
    TheatreHallViewSet,
    ReservationViewSet,
)

app_name = "catalog"

router = DefaultRouter()
router.register("plays", PlayViewSet, basename="plays")
router.register("actors", ActorViewSet, basename="actors")
router.register("genres", GenreViewSet, basename="genres")
router.register("performances", PerformanceViewSet, basename="performances")
router.register("tickets", TicketViewSet, basename="tickets")
router.register("theatre-halls", TheatreHallViewSet, basename="theatre-halls")
router.register("reservations", ReservationViewSet, basename="reservations")
urlpatterns = [
    path("", include(router.urls)),
]
