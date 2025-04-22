from django.urls import path
from .views import dashboard, set_budget, insights
from . import views

app_name = 'finance'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('set-budget/', set_budget, name='set_budget'),
    path('insights/', insights, name='insights'),
    path('chatbot/', views.chatbot_response, name='chatbot-response'),
    path('chat/', views.chatbot_page, name='chatbot-page'),

]

