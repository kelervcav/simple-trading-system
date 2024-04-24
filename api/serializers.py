from rest_framework import serializers
from .models import Stock, Order


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'price', 'date_added']
        read_only_fields = ['date_added']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'stock', 'quantity', 'order_type', 'date_added']
        read_only_fields = ['user', 'date_added']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ['file']
