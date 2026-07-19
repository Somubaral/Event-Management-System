from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from tickets.models import (
    Ticket,
    TicketCategory
)
from bookings.services import BookingService
from payments.services import PaymentService
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from users.models import User
from venues.models import Venue
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from events.services import EventService
from tickets.models import TicketCategory
from django.contrib import messages
from django.shortcuts import render

from events.models import Event
from django.db.models import Sum
from bookings.models import Booking



def home(request):

    return render(
        request,
        "home.html"
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            return redirect("/")

        return render(
            request,
            "auth/login.html",
            {
                "error": "Invalid credentials"
            }
        )

    return render(
        request,
        "auth/login.html"
    )


def register_view(request):

    if request.method == "POST":

        User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"],
            role=request.POST["role"]
        )

        return redirect("login")

    return render(
        request,
        "auth/register.html"
    )


def logout_view(request):

    logout(request)

    return redirect("/")


def events_page(request):

    events = Event.objects.filter(
        status="ACTIVE"
    ).select_related(
        "venue"
    )

    return render(
        request,
        "attendee/events.html",
        {
            "events": events
        }
    )


def event_detail(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    categories = (
        TicketCategory.objects.filter(
            event=event
        )
    )

    return render(
        request,
        "attendee/event_detail.html",
        {
            "event": event,
            "categories": categories
        }
    )


@login_required
def create_booking(
    request,
    category_id
):

    if request.method != "POST":

        return redirect(
            "events"
        )

    quantity = int(
        request.POST.get(
            "quantity",
            1
        )
    )

    try:

        booking = (
            BookingService.create_booking(
                request.user,
                category_id,
                quantity
            )
        )

        return render(
            request,
            "attendee/booking_created.html",
            {
                "booking": booking
            }
        )

    except Exception as e:

        return render(
            request,
            "error.html",
            {
                "message": str(e)
            }
        )


@login_required
def payment_page(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == "GET":

        return render(
            request,
            "attendee/payment.html",
            {
                "booking": booking
            }
        )

    payment_result = request.POST.get(
        "payment_result"
    )

    try:

        result = (
            PaymentService.process_payment(
                booking.id,
                payment_result
            )
        )

        if payment_result == "SUCCESS":

            return render(
                request,
                "attendee/payment_success.html",
                {
                    "ticket": result["ticket"]
                }
            )

        return render(
            request,
            "attendee/payment_failed.html",
            {
                "booking": booking
            }
        )

    except Exception as e:

        return render(
            request,
            "error.html",
            {
                "message": str(e)
            }
        )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        "event",
        "ticket_category"
    )

    return render(
        request,
        "attendee/my_bookings.html",
        {
            "bookings": bookings
        }
    )


@login_required
def my_tickets(request):

    tickets = Ticket.objects.filter(
        booking__user=request.user
    ).select_related(
        "booking",
        "booking__event"
    )

    return render(
        request,
        "attendee/my_tickets.html",
        {
            "tickets": tickets
        }
    )



@login_required
def verify_ticket(request):

    ticket = None

    if request.method == "POST":

        code = request.POST.get(
            "ticket_code"
        )

        try:

            ticket = Ticket.objects.get(
                ticket_code=code
            )

        except Ticket.DoesNotExist:

            ticket = None

    return render(
        request,
        "organizer/verify_ticket.html",
        {
            "ticket": ticket
        }
    )



@login_required
def organizer_dashboard(request):

    events = Event.objects.filter(
        organizer=request.user
    )

    total_bookings = Booking.objects.filter(
        event__organizer=request.user
    ).count()

    total_revenue = (
        Booking.objects.filter(
            event__organizer=request.user,
            status="CONFIRMED"
        ).aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )

    return render(
        request,
        "organizer/dashboard.html",
        {
            "events": events,
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
        }
    )

@login_required
def organizer_venues(request):

    venues = Venue.objects.all()

    return render(
        request,
        "organizer/venues/list.html",
        {
            "venues": venues
        }
    )


@login_required
def create_venue(request):

    if request.method == "POST":

        Venue.objects.create(
            name=request.POST["name"],
            address=request.POST["address"],
            capacity=request.POST["capacity"]
        )

        return redirect(
            "organizer-venues"
        )

    return render(
        request,
        "organizer/venues/create.html"
    )

@login_required
def venue_availability(request):

    venues = Venue.objects.all()

    context = {
        "venues": venues
    }

    if request.method == "POST":

        venue_id = request.POST["venue_id"]

        start_time = parse_datetime(
            request.POST["start_time"]
        )

        end_time = parse_datetime(
            request.POST["end_time"]
        )

        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)

        if timezone.is_naive(end_time):
            end_time = timezone.make_aware(end_time)

        conflict = Event.objects.filter(
            venue_id=venue_id,
            status="ACTIVE",
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        context["checked"] = True
        context["available"] = not conflict

    return render(
        request,
        "organizer/venues/availability.html",
        context
    )


@login_required
def create_event(request):

    venues = Venue.objects.all()

    if request.method == "POST":

        try:

            venue = Venue.objects.get(
                id=request.POST["venue"]
            )

            start_time = parse_datetime(
                request.POST["start_time"]
            )

            end_time = parse_datetime(
                request.POST["end_time"]
            )

            if timezone.is_naive(start_time):
                start_time = timezone.make_aware(start_time)

            if timezone.is_naive(end_time):
                end_time = timezone.make_aware(end_time)

            print("START:", start_time, start_time.tzinfo)
            print("END:", end_time, end_time.tzinfo)
            print("NOW:", timezone.now(), timezone.now().tzinfo)

            EventService.validate_future_date(
                start_time
            )

            EventService.validate_time_range(
                start_time,
                end_time
            )

            EventService.validate_venue_conflict(
                venue,
                start_time,
                end_time
            )

            Event.objects.create(
                organizer=request.user,
                venue=venue,
                title=request.POST["title"],
                description=request.POST["description"],
                start_time=start_time,
                end_time=end_time,
                status="ACTIVE"
            )

            return redirect(
                "organizer-dashboard"
            )

        except Exception as e:

            return render(
                request,
                "error.html",
                {
                    "message": str(e)
                }
            )

    return render(
        request,
        "organizer/events/create.html",
        {
            "venues": venues
        }
    )

@login_required
def event_bookings(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    bookings = Booking.objects.filter(
        event=event
    )

    return render(
        request,
        "organizer/events/bookings.html",
        {
            "event": event,
            "bookings": bookings
        }
    )

@login_required
def event_revenue(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    revenue = (
        Booking.objects.filter(
            event=event,
            status="CONFIRMED"
        ).aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )

    return render(
        request,
        "organizer/events/revenue.html",
        {
            "event": event,
            "revenue": revenue
        }
    )

@login_required
def ticket_categories(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    categories = TicketCategory.objects.filter(
        event=event
    )

    return render(
        request,
        "organizer/tickets/list.html",
        {
            "event": event,
            "categories": categories
        }
    )


@login_required
def create_ticket_category(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    if request.method == "POST":

        TicketCategory.objects.create(
            event=event,
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            total_quantity=request.POST.get("quantity"),
            available_quantity=request.POST.get("quantity")
        )

        return redirect(
            "organizer-event-tickets",
            event_id=event.id
        )

    return render(
        request,
        "organizer/create_ticket_category.html",
        {
            "event": event
        }
    )


@login_required
def edit_ticket_category(
    request,
    category_id
):

    category = get_object_or_404(
        TicketCategory,
        id=category_id
    )

    if category.event.organizer != request.user:

        return redirect(
            "organizer-dashboard"
        )

    if request.method == "POST":

        category.name = request.POST["name"]

        category.price = request.POST["price"]

        category.save()

        return redirect(
            "ticket-categories",
            event_id=category.event.id
        )

    return render(
        request,
        "organizer/tickets/edit.html",
        {
            "category": category
        }
    )

@login_required
def edit_event(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    if request.method == "POST":

        event.title = request.POST["title"]

        event.description = request.POST["description"]

        event.save()

        messages.success(
            request,
            "Event updated successfully."
        )

        return redirect(
            "organizer-dashboard"
        )

    return render(
        request,
        "organizer/events/edit.html",
        {
            "event": event
        }
    )

@login_required
def cancel_event(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    event.status = "CANCELLED"

    event.save()

    messages.success(
        request,
        "Event cancelled successfully."
    )

    return redirect(
        "organizer-dashboard"
    )

@login_required
def event_analytics(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    bookings = Booking.objects.filter(
        event=event
    )

    total_bookings = bookings.count()

    confirmed_bookings = bookings.filter(
        status="CONFIRMED"
    ).count()

    revenue = (
        bookings.filter(
            status="CONFIRMED"
        ).aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )

    tickets_sold = (
        bookings.filter(
            status="CONFIRMED"
        ).aggregate(
            total=Sum("quantity")
        )["total"]
        or 0
    )

    return render(
        request,
        "organizer/events/analytics.html",
        {
            "event": event,
            "total_bookings": total_bookings,
            "confirmed_bookings": confirmed_bookings,
            "tickets_sold": tickets_sold,
            "revenue": revenue
        }
    )

@login_required
def organizer_event_bookings(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    bookings = Booking.objects.filter(
        event=event
    ).select_related(
        "user",
        "ticket_category"
    )

    return render(
        request,
        "organizer/event_bookings.html",
        {
            "event": event,
            "bookings": bookings
        }
    )


@login_required
def organizer_event_revenue(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    revenue = (
        Booking.objects.filter(
            event=event,
            status="CONFIRMED"
        ).aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )

    booking_count = Booking.objects.filter(
        event=event
    ).count()

    return render(
        request,
        "organizer/event_revenue.html",
        {
            "event": event,
            "revenue": revenue,
            "booking_count": booking_count
        }
    )

@login_required
def organizer_event_tickets(
    request,
    event_id
):

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer=request.user
    )

    categories = TicketCategory.objects.filter(
        event=event
    )

    return render(
        request,
        "organizer/tickets.html",
        {
            "event": event,
            "categories": categories
        }
    )
