from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class MembershipType(models.TextChoices):
    BASIC = 'BS', 'Basic'
    PREMIUM = 'PR', 'Premium' 
    STUDENT = 'ST', 'Student'


class Genre(models.TextChoices):
    FANTASY = 'FT', 'Fantasy'
    SCIENCE_FICTION = 'SF', 'Science Fiction'
    ROMANCE = 'RM', 'Romance'
    HORROR = 'HR', 'Horror'
    HISTORICAL = 'HS', 'Historical'


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=100, unique=True)
    membership_type = models.CharField(
        max_length=2, 
        choices=MembershipType.choices,
        default=MembershipType.BASIC
    )
    join_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  
    total_borrowed = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200) 
    author = models.CharField(max_length=60)
    genre = models.CharField(max_length=2, choices=Genre.choices)
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2026)]
    )
    quantity_total = models.IntegerField(validators=[MinValueValidator(1)])
    quantity_available = models.IntegerField(validators=[MinValueValidator(0)])  # NEW: Track available
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_rare = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_records' 
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='borrow_history'
    )
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  
    late_fee = models.DecimalField(
        max_digits=6,  
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    is_returned = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.member} borrowed {self.book}"