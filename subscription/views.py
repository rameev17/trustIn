from django.http import JsonResponse
from .models import SubscriptionPlan

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