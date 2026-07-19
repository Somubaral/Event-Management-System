from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),

    path(
        "events/",
        events_page,
        name="events"
    ),

    path(
        "event/<int:event_id>/",
        event_detail,
        name="event-detail"
    ),

    path(
        "book/<int:category_id>/",
        create_booking,
        name="create-booking"
    ),

    path(
        "payment/<int:booking_id>/",
        payment_page,
        name="payment-page"
    ),

    path(
        "my-bookings/",
        my_bookings,
        name="my-bookings"
    ),

    path(
        "my-tickets/",
        my_tickets,
        name="my-tickets"
    ),

    path(
        "organizer/dashboard/",
        organizer_dashboard,
        name="organizer-dashboard"
    ),

    path(
        "organizer/verify-ticket/",
        verify_ticket,
        name="verify-ticket"
    ),

path(
    "login/",
    login_view,
    name="login"
),

path(
    "register/",
    register_view,
    name="register"
),

path(
    "logout/",
    logout_view,
    name="logout"
),


path(
    "organizer/venues/",
    organizer_venues,
    name="organizer-venues"
),

path(
    "organizer/venues/create/",
    create_venue,
    name="create-venue"
),

path(
    "organizer/venues/availability/",
    venue_availability,
    name="venue-availability-page"
),

path(
    "organizer/events/create/",
    create_event,
    name="create-event"
),

path(
    "organizer/event/<int:event_id>/bookings/",
    event_bookings,
    name="event-bookings"
),

path(
    "organizer/event/<int:event_id>/revenue/",
    event_revenue,
    name="event-revenue"
),

path(
    "organizer/event/<int:event_id>/tickets/",
    ticket_categories,
    name="ticket-categories"
),

path(
    "organizer/event/<int:event_id>/tickets/create/",
    create_ticket_category,
    name="create-ticket-category"
),

path(
    "organizer/ticket-category/<int:category_id>/edit/",
    edit_ticket_category,
    name="edit-ticket-category"
),

path(
    "organizer/event/<int:event_id>/edit/",
    edit_event,
    name="edit-event"
),

path(
    "organizer/event/<int:event_id>/cancel/",
    cancel_event,
    name="cancel-event"
),

path(
    "organizer/event/<int:event_id>/analytics/",
    event_analytics,
    name="event-analytics"
),

path(
    "organizer/event/<int:event_id>/bookings/",
    organizer_event_bookings,
    name="organizer-event-bookings"
),

path(
    "organizer/event/<int:event_id>/revenue/",
    organizer_event_revenue,
    name="organizer-event-revenue"
),

path(
    "organizer/event/<int:event_id>/tickets/",
    organizer_event_tickets,
    name="organizer-event-tickets"
),







]