from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, date
from .models import Transaction
from .forms import TransactionForm

@login_required
def dashboard(request):
    today = timezone.now().date()  # Get today's date
    current_year = today.year
    current_month = today.month

    # Get all transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user)

    # Default filters (current year and month)
    year_filter = request.GET.get('year', current_year)
    month_filter = request.GET.get('month', current_month)
    category_filter = request.GET.get('category', None)

    # Apply the filters based on user input
    if year_filter:
        transactions = transactions.filter(fake_date__year=year_filter)

    if month_filter:
        transactions = transactions.filter(fake_date__month=month_filter)

    if category_filter:
        transactions = transactions.filter(category=category_filter)

    # Filter out transactions that are in the future
    transactions = transactions.filter(fake_date__lte=today)

    # Handle form submission for new transactions
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Ensure the logged-in user is saved with the transaction

            # Get the recurrence type
            recurrence = transaction.recurring
            today = timezone.now().date()  # Get today's date

            # Define the recurrence logic
            if recurrence == "weekly":
                start_date = today
                end_date = date(2025, 12, 31)  # End of 2025
                while start_date <= end_date:
                    fake_date = start_date
                    Transaction.objects.create(
                        user=request.user,
                        amount=transaction.amount,
                        category=transaction.category,
                        description=transaction.description,
                        recurring=transaction.recurring,
                        fake_date=fake_date
                    )
                    start_date += timedelta(weeks=1)

            elif recurrence == "biweekly":
                start_date = today
                end_date = date(2025, 12, 31)
                while start_date <= end_date:
                    fake_date = start_date
                    Transaction.objects.create(
                        user=request.user,
                        amount=transaction.amount,
                        category=transaction.category,
                        description=transaction.description,
                        recurring=transaction.recurring,
                        fake_date=fake_date
                    )
                    start_date += timedelta(weeks=2)

            elif recurrence == "monthly":
                start_date = today.replace(day=1)
                end_date = date(2025, 12, 31)
                while start_date <= end_date:
                    fake_date = start_date
                    Transaction.objects.create(
                        user=request.user,
                        amount=transaction.amount,
                        category=transaction.category,
                        description=transaction.description,
                        recurring=transaction.recurring,
                        fake_date=fake_date
                    )
                    if start_date.month == 12:
                        start_date = start_date.replace(year=start_date.year + 1, month=1)
                    else:
                        start_date = start_date.replace(month=start_date.month + 1)

            # Redirect back to the dashboard after creating the recurring transactions
            return redirect("finance:dashboard")

    else:
        form = TransactionForm()

    # Order transactions by fake_date (most recent first)
    transactions = transactions.order_by('-fake_date')

    # Pass data to the template
    return render(request, 'finance/dashboard.html', {
        'transactions': transactions,
        'form': form,
        'year_filter': year_filter,
        'month_filter': month_filter,
        'category_filter': category_filter
    })
