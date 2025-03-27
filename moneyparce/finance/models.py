from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.db import models


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ("income", "Income"),
        ("food", "Food"),
        ("rent", "Rent"),
        ("entertainment", "Entertainment"),
        ("misc", "Miscellaneous"),
    ]

    RECURRING_CHOICES = [
        ("one_time", "One-Time"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("biweekly", "Biweekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    recurring = models.CharField(
        max_length=10, choices=RECURRING_CHOICES, default="one_time"
    )

    fake_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Automatically set fake_date based on recurrence type."""
        if not self.fake_date:  # Only set if it's empty
            self.fake_date = self.calculate_fake_date()
        super().save(*args, **kwargs)

    def calculate_fake_date(self):
        """Determine fake_date based on recurring type."""
        today = now().date()
        if self.recurring == "monthly":
            return today.replace(day=1)
        elif self.recurring == "biweekly":
            return today.replace(day=1) if today.day <= 15 else today.replace(day=15)
        elif self.recurring == "weekly":
            if today.day <= 7:
                return today.replace(day=1)
            elif today.day <= 14:
                return today.replace(day=8)
            elif today.day <= 21:
                return today.replace(day=15)
            else:
                return today.replace(day=21)
        return today  # Default for one-time transactions

    def __str__(self):
        return f"{self.user.username} - {self.category} - ${self.amount} on {self.fake_date}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monthly budget amount
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the budget is created

    def __str__(self):
        return f"{self.user.username}'s budget: ${self.amount} per month"
