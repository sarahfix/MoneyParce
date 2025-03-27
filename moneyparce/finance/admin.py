from django.contrib import admin
from .models import Transaction, Budget  # Import the Budget model

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "date", "fake_date", "recurring", "description")
    list_filter = ("category", "recurring", "fake_date")
    search_fields = ("user__username", "category", "description")


class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "created_at")  # Display user, amount, and creation timestamp
    search_fields = ("user__username",)  # Allow searching by the user's username
    list_filter = ("user",)  # Filter budgets by user

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Budget, BudgetAdmin)  # Register the Budget model
