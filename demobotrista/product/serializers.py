from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product objects.
    """

    name = serializers.CharField(required=True)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(required=True)
    currency = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "currency",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate_price(self, value):
        """
        Ensure the price is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        """
        Ensure the stock count is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Product objects.
    """

    name = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(required=False)
    currency = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "currency",
        ]

    def validate_price(self, value):
        """
        Ensure the price is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        """
        Ensure the stock count is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
