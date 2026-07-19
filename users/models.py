from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ORGANIZER = "ORGANIZER"
    ATTENDEE = "ATTENDEE"

    ROLE_CHOICES = (
        (ORGANIZER, "Organizer"),
        (ATTENDEE, "Attendee"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return self.username

