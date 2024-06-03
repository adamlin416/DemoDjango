from django.db import transaction
from product.models import Product
from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem objects."""

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        """Check if the quantity is valid."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order objects."""

    items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ["id", "user", "items"]
        read_only_fields = ["user"]

    def validate_items(self, value):
        """Check if the items are valid."""
        if not value:
            raise serializers.ValidationError("Order must have items.")
        product_set = set()
        for item in value:
            if item["quantity"] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0.")
            if item["product"] in product_set:
                raise serializers.ValidationError("Duplicate products in order.")
            product_set.add(item["product"])
        return value

    def create(self, validated_data):
        # Make sure orders only created by users himself.
        validated_data["user"] = self.context["request"].user
        items_data = validated_data.pop("items")
        items_qt_map = {item["product"].id: item["quantity"] for item in items_data}
        with transaction.atomic():
            # Check if all products are in stock
            # Lock the products row for update
            product_ids = items_qt_map.keys()
            products = Product.objects.select_for_update().filter(id__in=product_ids)
            out_of_stock_products = []
            # Check if all product stocks are enough
            for product in products:
                if product.stock < items_qt_map[product.id]:
                    out_of_stock_products.append(product.name)
            if out_of_stock_products:
                raise serializers.ValidationError(
                    {
                        "detail": f"Products {', '.join(out_of_stock_products)} out of stock."
                    }
                )
            # Create order
            order = Order.objects.create(**validated_data)
            order_items = []
            # Create order items and update stock, use bulk for better performance
            for product in products:
                order_items.append(
                    OrderItem(
                        order=order, product=product, quantity=items_qt_map[product.id]
                    )
                )
                product.stock -= items_qt_map[product.id]
            OrderItem.objects.bulk_create(order_items)
            Product.objects.bulk_update(products, ["stock"])
            return order
