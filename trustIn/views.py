from django.http import JsonResponse
from .models import Report,Calendar,Sponsor,YearCalendar, Vacancy,News, Statistics, About, Team, TeamMember, Founder
from collections import defaultdict
from datetime import datetime
from django.db import models
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime
from django.db import models
from .models import Calendar, YearCalendar, Sponsor

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




@api_view(['GET'])
def get_active_calendars(request):
    active_calendars = Calendar.objects.filter(is_active=True)

    data = [
        {
            "id": cal.id,
            "title": cal.title,
            "image": request.build_absolute_uri(cal.image.url) if cal.image and cal.image.url else None,
            "is_active": cal.is_active
        }
        for cal in active_calendars
    ]

    return JsonResponse(data, safe=False, status=200)

@api_view(['GET'])
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

    data = [
        {
            "id": yc.id,
            "year": yc.year,
            "image": request.build_absolute_uri(yc.image.url) if yc.image and yc.image.url else None,
            "is_active": yc.is_active
        }
        for yc in year_calendars
    ]

    return JsonResponse(data, safe=False, status=200)

@api_view(['GET'])
def get_sponsors(request):
    sponsors = Sponsor.objects.filter(is_active=True)

    data = [
        {
            "id": sponsor.id,
            "image": request.build_absolute_uri(sponsor.image.url) if sponsor.image and sponsor.image.url else None
        }
        for sponsor in sponsors
    ]

    return JsonResponse(data, safe=False, status=200)
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
    
def statistics_view(request):
    if request.method == "GET":
        stats = Statistics.objects.first()

        data = {
            "students_count": stats.students_count if stats else 0,
            "donated_money": stats.donated_money if stats else 0,
            "donors_count": stats.donors_count if stats else 0
        }
        
        return JsonResponse(data, safe=False)


@api_view(['GET'])
def about_view(request):
    """
    API endpoint для получения данных страницы "О нас" с поддержкой мультиязычности.
    
    Query Parameters:
        locale (string): Язык контента. Возможные значения: 'kz' (казахский, по умолчанию), 'ru' (русский)
    """
    if request.method == 'GET':
        locale = request.query_params.get('locale', 'kz')
        
        # Валидация locale
        if locale not in ['kz', 'ru']:
            locale = 'kz'
        
        # Получаем данные для запрошенного языка (без fallback)
        about = About.objects.filter(locale=locale).first()
        
        # Если данных нет, возвращаем структуру с пустыми данными
        if not about:
            # Значения по умолчанию в зависимости от запрошенного языка
            if locale == 'kz':
                data = {
                    "title": "Бірлестік туралы",
                    "paragraphs": [],
                    "mission_title": "Біздің миссия",
                    "mission_text": "",
                    "goals_title": "Мақсатымыз:",
                    "goals": []
                }
            else:
                data = {
                    "title": "О нас",
                    "paragraphs": [],
                    "mission_title": "Наша миссия",
                    "mission_text": "",
                    "goals_title": "Наши цели:",
                    "goals": []
                }
            return Response(data, status=200)
        
        # Формируем ответ с данными из базы
        data = {
            "title": about.title,
            "paragraphs": [p.text for p in about.paragraphs.all().order_by('order')],
            "mission_title": about.mission_title,
            "mission_text": about.mission_text,
            "goals_title": about.goals_title,
            "goals": [g.text for g in about.goals.all().order_by('order')]
        }
        
        return Response(data, status=200)


@api_view(['GET'])
def team_view(request):
    """
    API endpoint для получения данных страницы "Команда" с поддержкой мультиязычности.
    
    Query Parameters:
        locale (string): Язык контента. Возможные значения: 'kz' (казахский, по умолчанию), 'ru' (русский)
    """
    if request.method == 'GET':
        locale = request.query_params.get('locale', 'kz')
        
        # Валидация locale
        if locale not in ['kz', 'ru']:
            locale = 'kz'
        
        # Получаем данные для запрошенного языка (без fallback)
        team = Team.objects.filter(locale=locale).first()
        
        # Если нет данных Team, используем значения по умолчанию для запрошенного языка
        if not team:
            team_title = "Біздің команда" if locale == 'kz' else "Наша команда"
            founders_title = "Бірлестіктің құрылтайшылары" if locale == 'kz' else "Основатели ассоциации"
        else:
            team_title = team.team_title
            founders_title = team.founders_title
        
        # Получаем активных членов команды для запрошенного языка (без fallback)
        team_members = TeamMember.objects.filter(locale=locale, is_active=True).order_by('order', 'name')
        
        # Получаем основателей для запрошенного языка (без fallback)
        founders = Founder.objects.filter(locale=locale).order_by('order', 'name')
        
        # Формируем ответ
        data = {
            "team_title": team_title,
            "team_members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "role": member.role,
                    "year": member.year,
                    "contact": member.contact,
                    "image": request.build_absolute_uri(member.image.url) if member.image and member.image.url else None
                }
                for member in team_members
            ],
            "founders_title": founders_title,
            "founders": [
                {
                    "name": founder.name
                }
                for founder in founders
            ]
        }
        
        return Response(data, status=200)