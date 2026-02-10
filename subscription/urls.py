from django.urls import path
from . import views

urlpatterns = [
    path('subscription-plans/', views.get_subscription_plans, name='get_subscription_plans'),
    path('increment-subscription/<int:plan_id>/', views.increment_subscription, name='increment_subscription'),


]