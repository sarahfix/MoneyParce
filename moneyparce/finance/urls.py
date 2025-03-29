from django.urls import path
from .views import dashboard, set_budget, insights

app_name = 'finance'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('set-budget/', set_budget, name='set_budget'),
    path('insights/', insights, name='insights'),# Ensure this line exists
]

