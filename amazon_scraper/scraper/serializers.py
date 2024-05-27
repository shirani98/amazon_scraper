from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)