from django.urls import path
from .views import dashboard

app_name = 'finance'  # This is important for namespacing

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),  # This must match the template reference
]
