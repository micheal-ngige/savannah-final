from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
import africastalking

# SMS Initialization
africastalking.initialize('sandbox', 'your_africastalking_api_key')
sms = africastalking.SMS

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save()
        # Sending SMS
        message = f"New order placed: {order.item} for {order.amount}."
        sms.send(message, [order.customer.code])
