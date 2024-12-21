from django.urls import path
from . import views

urlpatterns = [
    path('reports-grouped/', views.get_reports_grouped, name='get_reports_grouped'),
    path('sponsors/', views.get_sponsors, name='get_sponsors'),
    path('calendar-images/', views.get_active_calendars, name='get_active_calendars'),
    path('calendar-year/', views.get_year_calendars, name='get_year_calendars'),
    path("vacancies/", views.vacancy_list, name="vacancy_list"),
    path("news/", views.news_list, name="news_list"),


]