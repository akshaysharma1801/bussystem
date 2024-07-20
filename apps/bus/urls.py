from django.urls import path
from .views import (
    AddBusView, AddBusStopBy,
    BusSearchView, SeatBlockCreateView, 
    BookingCreateView
)

app_name = "bus"

urlpatterns = [
    path('add-bus/', AddBusView.as_view()),
    path('add-bus-stop/', AddBusStopBy.as_view()),
    path('search-buses/', BusSearchView.as_view(), name='search_buses'),

    path('seat-blocks/', SeatBlockCreateView.as_view(), name='seat_block_create'),
    path('bookings/', BookingCreateView.as_view(), name='booking_create'),
]
