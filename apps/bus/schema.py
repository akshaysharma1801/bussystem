from drf_yasg import openapi


add_bus_schema = openapi.Schema(
    title =("Add Bus"),
    type=openapi.TYPE_OBJECT, 
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING,example="Bus 1"),
        'total_seats': openapi.Schema(type=openapi.TYPE_INTEGER,example=50),
        'available_seats': openapi.Schema(type=openapi.TYPE_INTEGER,example=50),
        'source': openapi.Schema(type=openapi.TYPE_STRING,example="agra"),
        'source_start_time': openapi.Schema(type=openapi.TYPE_STRING,example="2024-07-25 18:00:00"),
        'destination': openapi.Schema(type=openapi.TYPE_STRING,example="gurgaon"),
        'destination_end_time': openapi.Schema(type=openapi.TYPE_STRING,example="2024-07-25 22:00:00"),
        'bus_number': openapi.Schema(type=openapi.TYPE_STRING,example="HR BB 05 1986"),
    },
    required=['name','total_seats','available_seats','source','source_start_time','destination',
              'destination_end_time','bus_number'],
)


add_bus_stop_schema = openapi.Schema(
    title =("Add Bus Stop"),
    type=openapi.TYPE_OBJECT, 
    properties={
        'bus_id': openapi.Schema(type=openapi.TYPE_INTEGER,example=4),
        'stop_name': openapi.Schema(type=openapi.TYPE_STRING,example="rajiv chowk"),
        'arrival_time': openapi.Schema(type=openapi.TYPE_STRING,example="2024-07-25 19:30:00"),
    },
    required=['bus_id','stop_name','arrival_time'],
)

block_seat_schema = openapi.Schema(
    title =("Block Seat"),
    type=openapi.TYPE_OBJECT, 
    properties={
        'bus': openapi.Schema(type=openapi.TYPE_INTEGER,example=4),
        'stop': openapi.Schema(type=openapi.TYPE_INTEGER,example=5),
        'no_of_passengers': openapi.Schema(type=openapi.TYPE_INTEGER,example=5),
    },
    required=['bus_id','stop_name','arrival_time'],
)

book_ticket_schema = openapi.Schema(
    title =("Book ticket"),
    type=openapi.TYPE_OBJECT, 
    properties={
        'seat_block_id': openapi.Schema(type=openapi.TYPE_STRING,example="BLH9940200724"),
    },
    required=['seat_block_id','stop_name','arrival_time'],
)