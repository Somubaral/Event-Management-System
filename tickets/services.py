from .models import TicketCategory


class TicketCategoryService:

    @staticmethod
    def create_ticket_category(validated_data):

        return TicketCategory.objects.create(
            **validated_data
        )