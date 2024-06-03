from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .permissions import CanOrderPermission
from .serializers import OrderSerializer


class OrderListAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), CanOrderPermission()]

    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="orders_list",
        request=None,
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request):
        """Return a list of all orders. Only managers can list all orders."""
        if request.user.groups.filter(name="Manager").exists():
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=OrderSerializer,
        responses={201: OrderSerializer},
    )
    def post(self, request):
        """Create a new order. Only customers can create orders."""

        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
