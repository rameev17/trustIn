from django.http import JsonResponse
from .models import SubscriptionPlan

def get_subscription_plans(request):
    if request.method == 'GET':
        # Retrieve active subscription plans with hover_image
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price').values(
            'id', 'title', 'price', 'image', 'hover_image', 'is_active','active_sub_count'
        )
        
        # Build the response to include both the main image and the hover image (if available)
        response_data = []
        for plan in plans:
            # Check if hover image exists, if not, return None for hover image
            plan_data = {
                'id': plan['id'],
                'title': plan['title'],
                'price': str(plan['price']),  # Convert decimal to string for better JSON handling
                'image': plan['image'],
                'hover_image': plan['hover_image'] if plan['hover_image'] else None,
                'is_active': plan['is_active'],
                'active_sub_count':plan['active_sub_count']
            }
            response_data.append(plan_data)

        return JsonResponse(response_data, safe=False)