from django.http import JsonResponse
from .models import Report,Calendar,Sponsor,YearCalendar, Vacancy,News
from collections import defaultdict
from datetime import datetime
from django.db import models
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

def get_reports_grouped(request):
    if request.method == 'GET':
        reports = Report.objects.values('id', 'title', 'file', 'month', 'year', 'created_at')
        grouped_reports = defaultdict(lambda: defaultdict(list))

        for report in reports:
            year = report['year']
            month = report['month'] or "Yearly"
            grouped_reports[year][month].append({
                "id": report['id'],
                "title": report['title'],
                "file": report['file'],
                "created_at": report['created_at']
            })

        return JsonResponse({k: dict(v) for k, v in grouped_reports.items()}, safe=False)




def get_active_calendars(request):
    active_calendars = Calendar.objects.filter(is_active=True)
    data = list(active_calendars.values('id', 'title', 'image', 'is_active'))
    return JsonResponse(data, safe=False)


def get_year_calendars(request):
    current_year = datetime.now().year
    year_calendars = YearCalendar.objects.filter(is_active=True).order_by(
        models.Case(
            models.When(year=current_year, then=0),
            default=1,
            output_field=models.IntegerField(),
        ),
        'year'
    )

    data = list(year_calendars.values('id', 'year', 'image', 'is_active'))
    return JsonResponse(data, safe=False)
def get_sponsors(request):
    if request.method == 'GET':
        sponsors = Sponsor.objects.filter(is_active=True).values('id', 'image')
        return JsonResponse(list(sponsors), safe=False)

@csrf_exempt
def vacancy_list(request):
    if request.method == "GET":
        vacancy_id = request.GET.get("id")

        if vacancy_id:
            try:
                vacancy = Vacancy.objects.get(id=vacancy_id, is_active=True)
                vacancy_data = {
                    "id": vacancy.id,
                    "company_info": vacancy.company_info,
                    "position": vacancy.position,
                    "candidate_requirements": vacancy.candidate_requirements,
                    "responsibilities": vacancy.responsibilities,
                    "conditions": vacancy.conditions,
                    "contact_info": vacancy.contact_info,
                }
                return JsonResponse(vacancy_data)
            except Vacancy.DoesNotExist:
                return JsonResponse({"error": "Вакансия не найдена"}, status=404)

        try:
            page_number = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 10))
        except ValueError:
            return JsonResponse({"error": "Invalid page or page_size parameter"}, status=400)

        vacancies = Vacancy.objects.filter(is_active=True)

        paginator = Paginator(vacancies, page_size)
        page = paginator.get_page(page_number)

        vacancy_data = [
            {
                "id": vacancy.id,
                "company_info": vacancy.company_info,
                "position": vacancy.position,
                "candidate_requirements": vacancy.candidate_requirements,
                "responsibilities": vacancy.responsibilities,
                "conditions": vacancy.conditions,
                "contact_info": vacancy.contact_info,
            }
            for vacancy in page
        ]

        return JsonResponse({
            "vacancies": vacancy_data,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "total_vacancies": paginator.count
        }, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            vacancy = Vacancy.objects.create(
                company_info=data.get("company_info"),
                position=data.get("position"),
                candidate_requirements=data.get("candidate_requirements"),
                responsibilities=data.get("responsibilities"),
                conditions=data.get("conditions"),
                contact_info=data.get("contact_info"),
                is_active=data.get("is_active", False),
            )
            return JsonResponse(
                {"message": "Вакансия успешно создана", "id": vacancy.id},
                status=201
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def news_list(request):
    if request.method == "GET":
        news_id = request.GET.get("id")
        page_number = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        news_queryset = News.objects.filter(is_active=True)

        if news_id:
            try:
                news_item = news_queryset.get(id=news_id)
                data = [
                    {
                        "id": news_item.id,
                        "title": news_item.title,
                        "description": news_item.description,
                        "image": request.build_absolute_uri(news_item.image.url) if news_item.image else None,
                        "is_active": news_item.is_active,
                        "created_at": news_item.created_at,
                    }
                ]
                return JsonResponse(data, safe=False)

            except News.DoesNotExist:
                return JsonResponse({"error": "Новость не найдена"}, status=404)

        paginator = Paginator(news_queryset, page_size)
        page = paginator.get_page(page_number)

        data = [
            {
                "id": news.id,
                "title": news.title,
                "description": news.description,
                "image": request.build_absolute_uri(news.image.url) if news.image else None,
                "is_active": news.is_active,
                "created_at": news.created_at,
            }
            for news in page
        ]

        response_data = {
            "news": data,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "total_news": paginator.count,
        }

        return JsonResponse(response_data, safe=False)