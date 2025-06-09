from django.conf import settings
from django.db import models
from catalog.utils.upload_paths import play_image_path, theatre_image_path


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to=play_image_path)
    actors = models.ManyToManyField("Actor", related_name="plays")
    genres = models.ManyToManyField("Genre", related_name="plays")


    def __str__(self):
        return f"{self.title}, {self.description}"


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey("TheatreHall", on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play}, {self.theatre_hall}, {self.show_time}"

    @property
    def total_capacity(self):
        return self.theatre_hall.capacity


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, null=True, related_name="tickets"
    )

    class Meta:
        unique_together = (
            "performance",
            "row",
            "seat",
        )
        ordering = ("seat",)

    @staticmethod
    def validate_seat(seat: int, max_seats: int, error_to_raise):
        if not (1 <= seat <= max_seats):
            raise error_to_raise(
                {
                    "seat": f"seat must be in range [1, {max_seats}], not {seat}",
                }
            )

    def clean(self):
        Ticket.validate_seat(
            self.seat, self.performance.theatre_hall.seats_in_row, ValueError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.row}, {self.seat}, {self.performance}, {self.reservation}"


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    image = models.ImageField(null=True, upload_to=theatre_image_path)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, null=True, related_name="reservations"
    )

    def __str__(self):
        return f"{self.created_at}, {self.user}"
