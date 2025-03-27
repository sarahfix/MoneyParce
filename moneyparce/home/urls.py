from django.urls import path
from . import views
from .views import settings_view  # Make sure this line is here

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path("settings/", settings_view, name="settings"),
]