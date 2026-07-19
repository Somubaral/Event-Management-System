from .models import Venue


class VenueService:

    @staticmethod
    def create_venue(validated_data):
        return Venue.objects.create(
            **validated_data
        )