from django.urls import path
from . import views

urlpatterns = [
    path('subscription-plans/', views.get_subscription_plans, name='get_subscription_plans'),
]