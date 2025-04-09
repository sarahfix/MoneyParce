from django.urls import path
from . import views
from .views import delete_account  # Ensure this line is present

urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),  # Use 'logout' instead of 'logout_view'
    path('delete/', views.delete_account, name='accounts.delete'),  # Maintain the "accounts.delete" format
    path('reset-password/', views.reset_password, name='reset_password')
]