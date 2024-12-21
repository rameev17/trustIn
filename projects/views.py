from django.http import JsonResponse
from .models import Project
from django.utils import timezone
from django.core.paginator import Paginator

def get_all_active_projects(request):
    if request.method == 'GET':
        active_projects = Project.objects.filter(is_active=True).order_by('ending_at')
        active_projects_count = active_projects.count()

        if active_projects_count < 4:
            inactive_projects = Project.objects.filter(is_active=False).order_by('created_at')
            combined_projects = list(active_projects) + list(inactive_projects[:4 - active_projects_count])
        else:
            combined_projects = list(active_projects[:4])

        data = [
            {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                "image": request.build_absolute_uri(project.image.url) if project.image else None,
                'donated_money': project.donated_money,
                'goal_money': project.goal_money,
                'ending_at': project.ending_at,
                'created_at': project.created_at
            }
            for project in combined_projects
        ]

        return JsonResponse(data, safe=False)

def project_list(request):
    if request.method == "GET":
        project_id = request.GET.get("id")
        status = request.GET.get("status")  

        if project_id:
            try:
                project = Project.objects.get(id=project_id, is_active=True)
                project_data = {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "image": request.build_absolute_uri(project.image.url) if project.image else None,
                    "donated_money": project.donated_money,
                    "goal_money": project.goal_money,
                    "ending_at": project.ending_at,
                    "created_at": project.created_at,
                }
                return JsonResponse(project_data)
            except Project.DoesNotExist:
                return JsonResponse({"error": "Project not found"}, status=404)

        current_time = timezone.now()
        projects = Project.objects.all()

        projects_to_deactivate = projects.filter(ending_at__lt=current_time)
        projects_to_deactivate.update(is_active=False)

        if status == "active":
            projects = projects.filter(is_active=True)
        elif status == "inactive":
            projects = projects.filter(is_active=False)

        page_number = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 10)
        paginator = Paginator(projects, page_size)
        page = paginator.get_page(page_number)

        data = [
            {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                "image": request.build_absolute_uri(project.image.url) if project.image else None,
                'donated_money': project.donated_money,
                'goal_money': project.goal_money,
                'ending_at': project.ending_at,
                'created_at': project.created_at
            }
            for project in page.object_list
        ]

        response_data = {
            "projects": data,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "total_projects": paginator.count,
        }

        return JsonResponse(response_data)