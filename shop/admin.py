from django.contrib import admin
from .models import Shop, Order

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')
    list_filter = ('is_active',)

@admin.register(Order)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_item', 'name', 'phone_number')
    list_filter = ('created_at',)