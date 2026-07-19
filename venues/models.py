from django.db import models


class Venue(models.Model):

    name = models.CharField(
        max_length=255
    )

    address = models.TextField()

    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name