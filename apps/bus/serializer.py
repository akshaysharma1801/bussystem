# serializers.py
from rest_framework import serializers
from .models import Bus,Stop, BusStop, SeatBlock, Booking


class BusSerializer(serializers.ModelSerializer):
    source_start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    destination_end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Bus
        fields = "__all__"

class BusStopCreateSerializer(serializers.Serializer):
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    stop_name = serializers.CharField(write_only=True)
    bus_id = serializers.IntegerField(required=True)

    class Meta:
        model = BusStop
        fields = ['id', 'bus', 'stop_name', 'arrival_time']

    def create(self, data):
        bus_id = self.context['request'].data.get('bus_id')
        stop_name = data.get('stop_name')
        arrival_time = data.get('arrival_time')

        try:
            bus = Bus.objects.get(id=bus_id)
        except Bus.DoesNotExist:
            raise serializers.ValidationError("Bus not found.")
        
        stop = Stop.objects.create(name = stop_name)
        bus_stop = BusStop.objects.create(stop=stop, bus = bus, arrival_time=arrival_time)
        
        if arrival_time < bus.source_start_time or arrival_time > bus.destination_end_time:
            raise serializers.ValidationError({"message":"Arrival time must be between the bus's source start time and destination end time.","success":False})

        data['bus_stop'] = bus_stop  
        data["bus"] = bus      
        return data
    
class StopSerializer(serializers.ModelSerializer):
    """Serializer for Stop model."""
    class Meta:
        model = Stop
        fields = ['id', 'name']
        
class BusStopSerializer(serializers.ModelSerializer):
    stop_name = serializers.CharField(source='stop.name', read_only=True)
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = BusStop
        fields = ['id', 'stop', 'stop_name', 'arrival_time']

class BusListSerializer(serializers.ModelSerializer):
    bus_stops = BusStopSerializer(many=True, read_only=True)

    class Meta:
        model = Bus
        fields = "__all__"



# Seat block and ticket booking
class SeatBlockSerializer(serializers.ModelSerializer):
    bus = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all())
    stop = serializers.PrimaryKeyRelatedField(queryset=Stop.objects.all())
    
    class Meta:
        model = SeatBlock
        fields = ['id', 'bus', 'stop', 'no_of_passengers', 'timestamp', 'block_id']
    
    def validate(self, data):
        bus = data.get('bus')
        no_of_passengers = data.get('no_of_passengers')
        if bus.available_seats < no_of_passengers:
            raise serializers.ValidationError('Not enough available seats on the bus.')
        return data

class BookingSerializer(serializers.ModelSerializer):
    seat_block_id = serializers.CharField()  # Use CharField to handle formatted ID

    class Meta:
        model = Booking
        fields = ['id', 'seat_block_id', 'timestamp', 'booking_id']

    def validate(self, data):
        seat_block_id = data.get('seat_block_id')
        if not SeatBlock.objects.filter(block_id=seat_block_id).exists():
            raise serializers.ValidationError({'seat_block_id': 'Seat block with this ID does not exist.'})
        return data