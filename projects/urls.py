from django.urls import path
from . import views

urlpatterns = [
    path('active-projects/', views.get_all_active_projects, name='get_all_active_projects'),
    path('projects/', views.project_list, name='project_by_id'),

]