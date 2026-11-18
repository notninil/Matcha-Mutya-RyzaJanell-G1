from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Cafe(models.Model):
    class PriceRange(models.TextChoices):
        BUDGET = "1", "₱ · Budget"
        MID = "2", "₱₱ · Mid-range"
        PREMIUM = "3", "₱₱₱ · Premium"

    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=80, default="Cebu City")
    price_range = models.CharField(max_length=1, choices=PriceRange, default=PriceRange.MID)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="cafes", limit_choices_to={"role": "owner"},
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    """One Explorer's visit to a café: the drink tried, a 1-5 rating and optional notes."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="checkins",
    )
    cafe = models.ForeignKey(Cafe, on_delete=models.PROTECT, related_name="checkins")
    drink_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    notes = models.TextField(blank=True, max_length=500)
    visited_on = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-visited_on", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "cafe", "visited_on"], name="checkins_one_per_cafe_per_day",
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5), name="checkins_rating_1_to_5",
            ),
        ]

    def __str__(self):
        return f"{self.user} @ {self.cafe} on {self.visited_on}"
