from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator


class EmployeePosition(models.TextChoices):
    ADMINISTRATOR = 'AD', 'Administrator'
    MANAGER = 'MG', 'Manager'
    RECEPTIONIST = 'RP', 'Receptionist'
    HOUSEKEEPER = 'HK', 'Housekeeper'
    LINE_COOK = 'LC', 'Line Cook'
    MAINTENANCE = 'MT', 'Maintenance Technician'
    SECURITY = 'SO', 'Security Officer'


class RoomQuality(models.TextChoices):
    BASIC = 'BS', 'Basic'
    CLASSIC = 'CL', 'Classic'
    PLUS = 'PL', 'Plus'
    FAMILY = 'FM', 'Family'
    LUXURY = 'LX', 'Luxury'


class RoomFloor(models.TextChoices):
    FIRST = '1F', 'First Floor'
    SECOND = '2F', 'Second Floor'
    THIRD = '3F', 'Third Floor'
    FOURTH = '4F', 'Fourth Floor'


class RoomStatus(models.TextChoices):
    VACANT = 'VT', 'Vacant'
    OCCUPIED = 'OC', 'Occupied'
    DIRTY = 'DT', 'Dirty'
    RESERVED = 'RS', 'Reserved'
    MAINTENANCE = 'MT', 'Maintenance'


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'


class Country(models.TextChoices):
    UZBEKISTAN = 'UZ', 'Uzbekistan'
    KAZAKHSTAN = 'KZ', 'Kazakhstan'
    RUSSIA = 'RU', 'Russia'
    UNITED_KINGDOM = 'GB', 'United Kingdom'
    AZERBAIJAN = 'AZ', 'Azerbaijan'
    GERMANY = 'DE', 'Germany'
    ITALY = 'IT', 'Italy'
    FRANCE = 'FR', 'France'


class BookingStatus(models.TextChoices):
    CONFIRMED = 'CF', 'Confirmed'
    PENDING = 'PD', 'Pending'
    CHECKED_IN = 'CI', 'Checked-In'
    CANCELLED = 'CL', 'Cancelled'
    NO_SHOW = 'NS', 'No-Show'


class ServiceCategory(models.TextChoices):
    DINING = 'DN', 'Dining'
    HOUSEKEEPING = 'HK', 'Housekeeping'
    TRANSPORT = 'TR', 'Transport'
    WELLNESS = 'WL', 'Wellness'
    BUSINESS = 'BS', 'Business'


class ServiceName(models.TextChoices):
    BREAKFAST = 'BR', 'Breakfast'
    LUNCH = 'LN', 'Lunch'
    CLEANING = 'CL', 'Cleaning'
    LAUNDRY = 'LD', 'Laundry'
    SHUTTLE = 'SH', 'Shuttle'
    VALET = 'VT', 'Valet'
    MASSAGE = 'MS', 'Massage'
    GYM = 'GM', 'Gym'
    PRINTING = 'PR', 'Printing'
    EVENTS = 'EV', 'Events'



class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)])
    position = models.CharField(max_length=2, choices=EmployeePosition.choices, default=EmployeePosition.RECEPTIONIST)
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_position_display()})"


class RoomType(models.Model):
    name = models.CharField(max_length=2, choices=RoomQuality.choices, default=RoomQuality.BASIC)
    description = models.TextField(validators=[MinLengthValidator(50), MaxLengthValidator(110)])
    capacity = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.get_name_display()


class Room(models.Model):
    STATUS_DESCRIPTIONS = {
        RoomStatus.VACANT: 'Clean and ready for check-in',
        RoomStatus.OCCUPIED: 'A guest is currently staying inside',
        RoomStatus.DIRTY: 'Needs housekeeping after a guest checks out',
        RoomStatus.RESERVED: 'Held for an upcoming guest arrival',
        RoomStatus.MAINTENANCE: 'Blocked for repairs and unavailable for booking',
    }

    room_number = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(499)])
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    floor = models.CharField(max_length=2, choices=RoomFloor.choices)
    status = models.CharField(max_length=2, choices=RoomStatus.choices, default=RoomStatus.VACANT)

    @property
    def status_description(self):
        return self.STATUS_DESCRIPTIONS.get(self.status, '')

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.get_name_display()})"


class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    gender = models.CharField(max_length=1, choices=Gender.choices)
    country = models.CharField(max_length=2, choices=Country.choices)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    registered_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    guests_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    status = models.CharField(max_length=2, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Booking #{self.id} - {self.guest}"


class Service(models.Model):
    name = models.CharField(max_length=2, choices=ServiceName.choices)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=2, choices=ServiceCategory.choices)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()


class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.service.get_name_display()} for Booking #{self.booking.id}"