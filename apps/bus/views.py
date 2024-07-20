from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Bus, SeatBlock, Booking
)
from rest_framework import generics
from apps.bus.serializer import (
    BusListSerializer,BusSerializer, 
    SeatBlockSerializer, BookingSerializer, 
    BusStopCreateSerializer
)
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class AddBusView(APIView):
    """ Add a new bus from source to destination and timing."""

    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request, *args, **kwargs):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Bus added successfully.", 
                             "data":serializer.data,
                             "success":True}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddBusStopBy(APIView):
    """ Add a new bus stop in the journey of bus travel."""

    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request, *args, **kwargs):
        serializer = BusStopCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                            "messsage": "Bus stop added successfully.",
                            "data":serializer.data,
                            "success":True},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BusListPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class BusSearchView(generics.ListAPIView):
    """ Search the list of buses from and to and date."""

    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = BusListSerializer
    pagination_class = BusListPagination
    queryset = Bus.objects.all()

    def get_queryset(self):
        
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        date = self.request.query_params.get('date', None)
        
        if source:
            queryset = self.queryset.filter(source__icontains=source)
        if destination:
            queryset = self.queryset.filter(destination__icontains=destination)
        if date:
            try:
                from datetime import datetime
                date = datetime.strptime(date, "%Y-%m-%d")
                start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
                end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
                queryset = queryset.filter(source_start_time__date__gte=start_of_day, destination_end_time__date__lte=end_of_day)
            except ValueError:
                return Response({"message":"Date format should be YYYY-MM-DD","success":False}, status=status.HTTP_400_BAD_REQUEST)

        return queryset
    
class SeatBlockCreateView(generics.CreateAPIView):
    """ Blocking of seat for a bus."""

    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = SeatBlockSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookingCreateView(generics.CreateAPIView):
    """ Book the ticket of a bus."""

    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            seat_block_id = serializer.validated_data['seat_block_id']
            try:
                seat_block = SeatBlock.objects.get(block_id=seat_block_id)
            except SeatBlock.DoesNotExist:
                return Response({"error": "Seat block not found"}, status=status.HTTP_404_NOT_FOUND)

            # Create the booking
            booking = Booking.objects.create(seat_block=seat_block)
            booking_serializer = self.get_serializer(booking)
            headers = self.get_success_headers(booking_serializer.data)
            return Response(booking_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)