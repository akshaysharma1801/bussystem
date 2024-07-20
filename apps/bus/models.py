from django.db import models
from django.utils import timezone
import random
import string

class Stop(models.Model):
    """Model representing a stop."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bus(models.Model):
    """Model representing a bus."""
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField(default=40)
    available_seats = models.PositiveIntegerField(default=40)
    source = models.CharField(max_length=100)
    source_start_time = models.DateTimeField()
    bus_number = models.CharField(max_length=100, default="")

    destination = models.CharField(max_length=100)
    destination_end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class BusStop(models.Model):
    """Model representing the stops of a bus."""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bus_stops')
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bus.name} at {self.stop.name} ({self.arrival_time})"

class SeatBlock(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    no_of_passengers = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    block_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.pk:  # if the object is being created (not updated)
            if self.bus.available_seats < self.no_of_passengers:
                raise ValueError('Not enough available seats')
            self.bus.available_seats -= self.no_of_passengers
            self.bus.save()
            self.block_id = self.generate_block_id()
        super().save(*args, **kwargs)

    def generate_block_id(self):
        date_str = self.timestamp.strftime('%d%m%y')
        random_str = ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.digits, k=4))
        return f"BL{random_str}{date_str}"

    def __str__(self):
        return f"Block {self.block_id} for {self.bus.name} at {self.stop.name}"

class Booking(models.Model):
    seat_block = models.OneToOneField(SeatBlock, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    booking_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.pk:  # if the object is being created (not updated)
            self.booking_id = self.generate_booking_id()
        super().save(*args, **kwargs)

    def generate_booking_id(self):
        date_str = self.timestamp.strftime('%d%m%y')
        random_str = ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.digits, k=4))
        return f"TK{random_str}{date_str}"

    def __str__(self):
        return f"Booking {self.booking_id} for block {self.seat_block.block_id}"
