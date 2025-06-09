from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from catalog.models import (
    Play,
    Actor,
    Genre,
    Performance,
    Ticket,
    TheatreHall,
    Reservation,
)
from catalog.permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    IsAuthenticatedUsersCanReservingTickets,
)
from catalog.serializers import (
    ActorSerializer,
    GenreSerializer,
    PerformanceSerializer,
    TheatreHallSerializer,
    PlayImageSerializer,
    PerformanceListSerializer,
    PlayListSerializer,
    PlayRetrieveSerializer,
    ActorWithPlaysSerializer,
    PerformanceRetrieveSerializer,
    TicketSerializer,
    TicketRetrieveSerializer,
    ReservationSerializer,
    TicketListSerializer,
    ReservationListSerializer,
    ReservationRetrieveSerializer,
    TheatreHallImageSerializer,
)
from catalog.utils.upload_image import handle_image_upload


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("actors")
        play_title = self.request.query_params.get("play", None)

        if play_title:
            queryset = queryset.filter(title__icontains=play_title)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "upload_image":
            return PlayImageSerializer
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayRetrieveSerializer
        return PlayRetrieveSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request):
        return handle_image_upload(self, request)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in [
            "list",
        ]:
            return ActorSerializer
        if self.action == "retrieve":
            return ActorWithPlaysSerializer
        return ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceRetrieveSerializer
        return PerformanceSerializer

    def get_queryset(self):
        return Performance.objects.select_related("play", "theatre_hall").annotate(
            sold_tickets=Count("tickets", filter=Q(tickets__reservation__isnull=False)),
            free_seats=F("theatre_hall__seats_in_row") * F("theatre_hall__rows")
                       - Count("tickets", filter=Q(tickets__reservation__isnull=False)),
            all_tickets=Count("tickets"),
            total_seats=ExpressionWrapper(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row"),
                output_field=IntegerField(),
            ),
        ).prefetch_related("tickets", "play__genres")


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list",):
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer

    def get_queryset(self):
        return Ticket.objects.select_related(
            "performance",
            "performance__play",
            "performance__theatre_hall",
            "reservation",
            "reservation__user",
        ).all()


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return TheatreHallImageSerializer
        return TheatreHallSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, *args, **kwargs):
        return handle_image_upload(self, request)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedUsersCanReservingTickets,)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        if self.action == "retrieve":
            return ReservationRetrieveSerializer
        return ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
