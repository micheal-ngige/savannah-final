from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer

class CustomerModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", code="12345")

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), "Test Customer")

class OrderModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", code="12345")
        self.order = Order.objects.create(customer=self.customer, item="Test Item", amount=99.99)

    def test_order_string_representation(self):
        self.assertEqual(str(self.order), "Order Test Item for Test Customer")

class CustomerViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Test Customer", code="12345")

    def test_get_customers(self):
        response = self.client.get(reverse('customer-list'))
        serializer = CustomerSerializer([self.customer], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_customer(self):
        response = self.client.post(reverse('customer-list'), {'name': 'New Customer', 'code': '67890'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.last().name, 'New Customer')

class OrderViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Test Customer", code="12345")
        self.order = Order.objects.create(customer=self.customer, item="Test Item", amount=99.99)

    def test_get_orders(self):
        response = self.client.get(reverse('order-list'))
        serializer = OrderSerializer([self.order], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order(self):
        response = self.client.post(reverse('order-list'), {'customer': self.customer.id, 'item': 'New Item', 'amount': 49.99})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.last().item, 'New Item')

    def test_order_sms_sent(self):
        # Here you can mock the SMS sending functionality if needed
        pass

class HomePageTests(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Welcome to the Home Page- Oauth2 works")
