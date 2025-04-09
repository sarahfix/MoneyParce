from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, date
from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm
from decimal import Decimal
from django.db import models
from django.utils.timezone import now, timedelta
from django.db.models import Sum


def insights(request):
    today = now().date()
    past_week = today - timedelta(days=6)  # Ensure past 7 full days

    # Get all one-time purchases (excluding income), using fake_date
    one_time_purchases = Transaction.objects.filter(
        user=request.user, fake_date__gte=past_week, recurring="one_time"
    ).exclude(category="income")

    # Calculate Spend Days (using fake_date)
    spend_days = {txn.fake_date for txn in one_time_purchases}

    # Generate all past week days & determine no-spend days
    all_days = {past_week + timedelta(days=i) for i in range(7)}
    no_spend_days = sorted(all_days - spend_days)

    # Format dates as "Day, Month Date"
    formatted_no_spend_days = [day.strftime("%A, %B %d") for day in no_spend_days]
    formatted_spend_days = [day.strftime("%A, %B %d") for day in spend_days]

    # Get Small Purchases (<$15, excluding income), using fake_date
    small_purchases = one_time_purchases.filter(amount__lt=15)
    small_purchases_count = small_purchases.count()
    small_purchases_total = small_purchases.aggregate(total=Sum("amount"))["total"] or 0
    small_purchases_list = small_purchases.values_list("description", flat=True)

    # Prepare data for small purchases chart
    if small_purchases.exists():
        small_purchases_by_day = one_time_purchases.filter(amount__lt=15).values('fake_date').annotate(
            total=Sum('amount'),
            count=models.Count('id')
        ).order_by('fake_date')
        small_purchases_chart_data = [['Date', 'Total Amount', 'Number of Purchases']]
        for item in small_purchases_by_day:
            small_purchases_chart_data.append([
                item['fake_date'].strftime("%Y-%m-%d"),
                float(item['total']),
                item['count']
            ])
    else:
        small_purchases_chart_data = [
            ['Date', 'Total Amount', 'Number of Purchases'],
            [today.strftime("%Y-%m-%d"), 0, 0]
        ]

    context = {
        "no_spend_days": formatted_no_spend_days,
        "spend_days": formatted_spend_days,
        "small_purchases_count": small_purchases_count,
        "small_purchases_total": small_purchases_total,
        "small_purchases_list": small_purchases_list,
        "small_purchases_chart_data": small_purchases_chart_data,
    }
    return render(request, "finance/insights.html", context)


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

    # Get the current month's budget, if set
    budget = Budget.objects.filter(user=request.user).first()

    # Initialize budget-related variables
    monthly_budget = 0
    monthly_spending = 0
    budget_status = ""
    target_spending = 0  # Set default to 0 if no budget exists

    if budget:
        monthly_budget = budget.amount
        days_in_month = (date(current_year, current_month + 1, 1) - date(current_year, current_month, 1)).days
        days_passed = today.day
        target_spending = monthly_budget * Decimal(days_passed) / Decimal(days_in_month)

        # Calculate current spending for this month (non-income transactions)
        monthly_spending = transactions.filter(
            fake_date__month=current_month,
            recurring__in=["one_time", "monthly", "weekly", "biweekly"]  # Include all recurring types
        ).exclude(
            category="income"  # Exclude income transactions
        ).aggregate(
            total_spent=models.Sum('amount')
        )['total_spent'] or 0

        # Determine over/under budget
        if monthly_spending > target_spending:
            budget_status = f"You are currently ${monthly_spending - target_spending:.2f} over budget."
        else:
            budget_status = f"You are currently ${target_spending - monthly_spending:.2f} under budget."

    # Category Spending Chart
    if transactions.exclude(category="income").exists():
        category_spending = transactions.exclude(category="income").values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        chart_data = [['Category', 'Amount']]
        for item in category_spending:
            chart_data.append([item['category'], float(item['total'])])
    else:
        chart_data = [['Category', 'Amount'], ['No Data', 1]]

    # Prepare budget progress data
    # Budget Progress Chart
    budget_progress_data = []
    if budget:
        budget_progress_data = [
            ['Type', 'Amount'],
            ['Spent', float(monthly_spending)],
            ['Remaining', float(max(monthly_budget - monthly_spending, 0))]
        ]

    # Time-Based Spending Chart
    if transactions.exclude(category="income").exists():
        time_spending = transactions.exclude(category="income").extra(
            {'day': "date(fake_date)"}
        ).values('day').annotate(
            total=Sum('amount')
        ).order_by('day')
        time_chart_data = [['Date', 'Amount']]
        for item in time_spending:
            time_chart_data.append([item['day'], float(item['total'])])
    else:
        time_chart_data = [['Date', 'Amount'], [today.strftime("%Y-%m-%d"), 0]]

    # Handle form submission for new transactions
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Ensure the logged-in user is saved with the transaction

            # **Explicitly Save One-Time Transactions**
            if transaction.recurring == "one_time":
                transaction.save()
                return redirect("finance:dashboard")

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
        'category_filter': category_filter,
        'monthly_budget': monthly_budget,
        'monthly_spending': monthly_spending,
        'budget_status': budget_status,
        'target_spending': target_spending,
        'chart_data': chart_data,
        'budget_progress_data': budget_progress_data,
        'time_chart_data': time_chart_data,
    })


@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            # Delete any existing budget for the user
            Budget.objects.filter(user=request.user).delete()

            # Save the new budget
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

            return redirect('finance:dashboard')  # Redirect to the dashboard
    else:
        # Pre-fill form with existing budget if available
        existing_budget = Budget.objects.filter(user=request.user).first()
        form = BudgetForm(instance=existing_budget) if existing_budget else BudgetForm()

    return render(request, 'finance/set_budget.html', {'form': form})