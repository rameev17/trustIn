from django.urls import path
from . import views

urlpatterns = [
    path('shop-items/', views.get_shop_items, name='get_shop_items'),
    path('create-order/', views.create_order, name='create_order'),

]