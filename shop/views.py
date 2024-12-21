from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Shop, Order
from .serializer import OrderSerializer

@api_view(['GET'])
def get_shop_items(request):
    if request.method == 'GET':
        items = Shop.objects.filter(is_active=True).values('id', 'title', 'price', 'image', 'is_active')
        return Response(items, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        item_id = request.data.get('id')
        name = request.data.get('name')
        phone_number = request.data.get('phoneNumber')

        try:
            shop_item = Shop.objects.get(id=item_id)
        except Shop.DoesNotExist:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            shop_item=shop_item,
            name=name,
            phone_number=phone_number
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)