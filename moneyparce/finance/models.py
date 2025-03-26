from django.db import models
from django.contrib.auth.models import User


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

    # Track whether this is one-time or recurring
    recurring = models.CharField(
        max_length=10,
        choices=RECURRING_CHOICES,
        default="one_time"
    )

    def __str__(self):
        return f"{self.user.username} - {self.category} - ${self.amount} ({self.get_recurring_display()})"


from django.db import models

# Create your models here.
