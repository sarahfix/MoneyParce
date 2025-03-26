from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "date", "fake_date", "recurring", "description")
    list_filter = ("category", "recurring", "fake_date")
    search_fields = ("user__username", "category", "description")

admin.site.register(Transaction, TransactionAdmin)
