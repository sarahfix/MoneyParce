from django import forms
from .models import Transaction, Budget

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'description', 'recurring']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'description']  # Use 'amount' instead of 'monthly_budget'

    amount = forms.DecimalField(  # Change this to 'amount'
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your max monthly budget'})
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Optional description for your budget'})
    )