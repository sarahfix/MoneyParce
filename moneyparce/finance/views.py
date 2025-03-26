from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)  # Only fetch user's data
    return render(request, 'finance/dashboard.html', {'transactions': transactions})