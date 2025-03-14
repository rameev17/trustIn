from django.contrib import admin
from .models import Report, Calendar, Sponsor, YearCalendar, Vacancy, News, Statistics

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'month', 'year', 'created_at')
    list_filter = ('year', 'month')
    search_fields = ('title',)

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_filter = ('is_active',)

class YearCalendarAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('year',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("position", "company_info", "contact_info")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ("students_count", "donated_money", "donors_count")
    
    def has_add_permission(self, request):
        """Разрешить добавление только одной записи"""
        if Statistics.objects.exists():
            return False  # Запрещаем добавлять новые записи
        return True

    def has_delete_permission(self, request, obj=None):
        """Запретить удаление записи"""
        return False
    
admin.site.register(YearCalendar, YearCalendarAdmin)