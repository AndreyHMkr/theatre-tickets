from django.db import transaction
from rest_framework import serializers
from catalog.models import (
    Play,
    Actor,
    Genre,
    Performance,
    Ticket,
    TheatreHall,
    Reservation,
)


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "title",
            "description",
        )


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Actor
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
        )


class PlayShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("title", "description")


class ActorWithPlaysSerializer(serializers.ModelSerializer):
    plays = PlayShortSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name", "plays")


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "title",
            "description",
            "image",
        )


class PlayRetrieveSerializer(serializers.ModelSerializer):
    actors = serializers.StringRelatedField(many=True, read_only=True)
    actor_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all(), write_only=True, source="actors"
    )

    class Meta:
        model = Play
        fields = ("title", "description", "actors", "actor_ids", "image")


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "image",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("play", "theatre_hall", "show_time")


class PerformanceListSerializer(serializers.ModelSerializer):
    play = serializers.StringRelatedField()
    theatre_hall = serializers.StringRelatedField()
    free_seats = serializers.IntegerField()

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play",
            "theatre_hall",
            "free_seats",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")

    def validate(self, attrs):
        Ticket.validate_seat(
            attrs["seat"],
            attrs["performance"].theatre_hall.seats_in_row,
            serializers.ValidationError,
        )
        return attrs


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("name", "rows", "seats_in_row", "image")


class TheatreHallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "image",
        )


class PerformanceRetrieveSerializer(serializers.ModelSerializer):
    theatre_hall = TheatreHallSerializer(read_only=True)
    sold_tickets = serializers.IntegerField()
    total_seats = serializers.IntegerField()
    taken_seat = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="seat", source="ticket_set"
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time",
            "total_seats",
            "taken_seat",
            "sold_tickets",
        )


class PerformToTicketSerializer(serializers.ModelSerializer):
    play = serializers.StringRelatedField()
    theatre_hall = serializers.StringRelatedField()

    class Meta:
        model = Performance
        fields = ("play", "theatre_hall", "show_time")


class TicketListSerializer(serializers.ModelSerializer):
    performance = PerformToTicketSerializer(read_only=True)
    reserved_by = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "reserved_by", "row", "seat", "performance")

    def get_reserved_by(self, obj):
        user = getattr(obj.reservation, "user", None)
        if user:
            return user.username if user.username else user.email
        return None


class TicketRetrieveSerializer(serializers.ModelSerializer):
    performance = PerformToTicketSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "created_at",
            "performance",
        )

    def get_created_at(self, obj):
        reservation = getattr(obj, "reservation", None)
        if reservation is None:
            return None
        user = getattr(obj.reservation, "user", None)
        if user:
            return {
                "created_at": reservation.created_at,
                "user": user.username if user.username else user.email,
            }
        return None


class TheatreHallListSerializer(TheatreHallSerializer):
    class Meta(TheatreHallSerializer.Meta):
        fields = ("name",)


class TicketCreateSerializer(serializers.ModelSerializer):
    performance = serializers.PrimaryKeyRelatedField(queryset=Performance.objects.all())

    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    class Meta(ReservationSerializer.Meta):
        fields = (
            "id",
            "created_at",
        )


class ReservationRetrieveSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=False, allow_empty=False)

    class Meta(ReservationSerializer.Meta):
        fields = (
            "id",
            "created_at",
            "tickets",
        )
