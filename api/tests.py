from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Stock, Order


class StockViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def add_stock(self):
        stock = Stock(name='TEST1', price='10')
        stock.save()

    def test_stock_list(self):
        self.add_stock()
        response = self.client.get('/api/stocks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stock_create(self):
        payload = {
            "name": "TEST",
            "price": 25
        }
        response = self.client.post('/api/stocks/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_stock_retrieve(self):
        self.add_stock()
        response = self.client.get('/api/stocks/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='password123')
        self.client.login(username='user1', password='password123')
        self.stock = Stock.objects.create(name='TEST', price='10')

    def test_order_list_by_user(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_create(self):
        payload = {
            "stock": self.stock.pk,
            "quantity": 5,
            "order_type": "BUY"
        }
        response = self.client.post('/api/orders/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        self.client.logout()


class OrdersFileUploadViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='password123')
        self.client.login(username='user1', password='password123')

    def test_file_upload(self):
        csv = "stock,quantity,order_type" \
              "2,50,BUY" \
              "2,10,BUY"
        csv_file = SimpleUploadedFile("sample.csv", csv.encode(), content_type="text/csv")
        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "Data imported successfully"})

    def test_invalid_file_format_upload(self):
        csv = "stock,quantity,order_type"
        csv_file = SimpleUploadedFile("sample.txt", csv.encode(), content_type="text/csv")
        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.client.logout()
