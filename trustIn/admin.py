from django.contrib import admin
from .models import Report, Calendar, Sponsor, YearCalendar, Vacancy, News, Statistics, About, AboutParagraph, AboutGoal, Team, TeamMember, Founder

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


class AboutParagraphInline(admin.TabularInline):
    model = AboutParagraph
    extra = 1
    ordering = ['order']


class AboutGoalInline(admin.TabularInline):
    model = AboutGoal
    extra = 1
    ordering = ['order']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'locale', 'created_at', 'updated_at')
    list_filter = ('locale', 'created_at')
    search_fields = ('title', 'mission_title', 'goals_title')
    inlines = [AboutParagraphInline, AboutGoalInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('locale', 'title')
        }),
        ('Миссия', {
            'fields': ('mission_title', 'mission_text')
        }),
        ('Цели', {
            'fields': ('goals_title',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_title', 'founders_title', 'locale', 'created_at', 'updated_at')
    list_filter = ('locale', 'created_at')
    search_fields = ('team_title', 'founders_title')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('locale', 'team_title', 'founders_title')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'year', 'contact', 'locale', 'is_active', 'order')
    list_filter = ('locale', 'is_active', 'created_at')
    search_fields = ('name', 'role', 'contact')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('locale', 'name', 'role', 'year', 'contact', 'image')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ('name', 'locale', 'order', 'created_at')
    list_filter = ('locale', 'created_at')
    search_fields = ('name',)
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('locale', 'name', 'order')
        }),
    )