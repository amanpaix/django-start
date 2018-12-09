from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Flight, Passenger
from django.urls import reverse
# Create your views here.
def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passenger": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        render(request, "flights/error.html", {"message": "Invalid methond"})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "no flight"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "no flight"})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
