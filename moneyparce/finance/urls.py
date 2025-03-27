from django.urls import path
from .views import dashboard, set_budget

app_name = 'finance'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('set-budget/', set_budget, name='set_budget'),  # Add this line
]
