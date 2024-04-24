import csv
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Stock, Order
from .serializers import StockSerializer, OrderSerializer, FileUploadSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
        Stock Endpoints
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
        Order Endpoints
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_type', 'stock']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
            List of order filter by User
        """
        queryset = self.filter_queryset(self.get_queryset())

        filtered_queryset = queryset.filter(user=self.request.user)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StockInvestmentView(RetrieveAPIView):
    """
        Total Stock Investment
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        stock_id = self.kwargs.get('stock_id')
        queryset = Order.objects.filter(user=user, stock_id=stock_id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_orders = []
        order_quantity = []
        stock_name = ""
        for order in queryset:
            value = order.quantity * order.stock.price
            stock_name = order.stock.name
            order_quantity.append(order.quantity)
            total_orders.append(value)

        response = {
            "stock_name": stock_name,
            "total_orders": sum(order_quantity),
            "total_price": sum(total_orders)
        }
        return Response(response)


class OrdersFileUploadView(CreateAPIView):
    """
        CSV file upload
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_file = serializer.validated_data['file']

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'Not a CSV file'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                # Get stock instance
                stock = Stock.objects.get(id=int(row['stock']))

                # Create Order
                Order.objects.create(
                    user=self.request.user,
                    stock=stock,
                    quantity=row['quantity'],
                    order_type=row['order_type']
                )
            return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
