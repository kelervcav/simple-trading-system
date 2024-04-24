from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import StockViewSet, OrderViewSet, StockInvestmentView, OrdersFileUploadView


router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stocks/<int:stock_id>/investment/', StockInvestmentView.as_view(), name='stock-investment'),
    path('upload/', OrdersFileUploadView.as_view(), name='order-upload-file')
]