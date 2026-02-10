from django.http import JsonResponse
from .models import SubscriptionPlan
from rest_framework.decorators import api_view
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from .models import SubscriptionPlan
import requests
import json
from django.conf import settings



TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID

@api_view(['GET'])
def get_subscription_plans(request):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')

    response_data = [
        {
            "id": plan.id,
            "title": plan.title,
            "price": str(plan.price),  # Convert decimal to string
            "image": request.build_absolute_uri(plan.image.url) if plan.image and plan.image.url else None,
            "hover_image": request.build_absolute_uri(plan.hover_image.url) if plan.hover_image and plan.hover_image.url else None,
            "is_active": plan.is_active,
            "active_sub_count": plan.active_sub_count
        }
        for plan in plans
    ]

    return JsonResponse(response_data, safe=False, status=200)


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Telegram error: {e}")

@csrf_exempt
@require_POST
def increment_subscription(request, plan_id):
    try:
        plan = SubscriptionPlan.objects.get(pk=plan_id)
    except SubscriptionPlan.DoesNotExist:
        raise Http404("Subscription plan not found")

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    first_name = escape(body.get("firstName", ""))
    last_name = escape(body.get("lastName", ""))
    year = escape(body.get("year", ""))
    phone = escape(body.get("phone", ""))
    email = escape(body.get("email", ""))

    plan.active_sub_count += 1
    plan.save()

    message = (
        f"🎉 <b>Новая подписка!</b>\n\n"
        f"📦 <b>План:</b> {plan.title}\n"
        f"💰 <b>Цена:</b> {plan.price} ₸\n"
        f"🔢 <b>Всего активных:</b> {plan.active_sub_count}\n\n"
        f"👤 <b>Имя:</b> {first_name} {last_name}\n"
        f"🎓 <b>Год выпуска:</b> {year}\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"📧 <b>Email:</b> {email}"
    )

    send_telegram_message(message)

    return JsonResponse({
        "status": "success",
        "active_sub_count": plan.active_sub_count
    })