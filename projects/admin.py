from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'donated_money', 'ending_at', 'is_active')
    list_filter = ('is_active', 'ending_at')
    search_fields = ('title', 'description')