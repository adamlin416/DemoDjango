from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .permissions import CanManageProductsPermission
from .serializers import ProductSerializer, ProductUpdateSerializer


class ProductListAPIView(APIView):
    """List all products or create a new product."""

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), CanManageProductsPermission()]

    @extend_schema(
        operation_id="products_list",
        request=None,
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request):
        """Return a list of all products. Filter by price or stock if provided."""
        price = request.query_params.get("price")
        stock = request.query_params.get("stock")
        query = Q()
        if price:
            query &= Q(price=price)
        if stock:
            query &= Q(stock=stock)
        products = Product.objects.filter(query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ProductSerializer,
        responses={201: ProductSerializer},
    )
    def post(self, request):
        """Create a new product. Only manager group users can create products."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetailAPIView(APIView):
    """Retrieve, update or delete a product."""

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), CanManageProductsPermission()]

    @extend_schema(
        request=None,
        responses={200: ProductSerializer},
    )
    def get(self, request, pk):
        """Get a product by ID."""
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @extend_schema(
        request=ProductUpdateSerializer,
        responses={200: ProductUpdateSerializer},
    )
    def put(self, request, pk):
        """Update a product by ID. Only manager group users can update products."""
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """Delete a product by ID. Only manager group users can delete products."""
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=204)
