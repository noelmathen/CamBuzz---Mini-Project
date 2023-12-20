#vehiclepooling/models.py
from django.db import models
from student.models import Student  # Import Student model from the student app
from django.core.validators import MinValueValidator

class VehicleListing(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    VEHICLE_TYPES = (
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Scooty', 'Scooty'),
    )
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    extra_helmet = models.BooleanField(default=False)
    vehicle_number = models.CharField(max_length=15)
    vehicle_name = models.CharField(max_length=100, default='')
    seats_available = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=1000, blank=False)

    def save(self, *args, **kwargs):
        if self.start_date > self.end_date:
            raise ValueError("End date must be after the start date")
        elif self.start_date == self.end_date and self.start_time >= self.end_time:
            raise ValueError("End time must be after the start time")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner}'s Vehicle Listing"


