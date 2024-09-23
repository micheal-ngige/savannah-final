from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.item} for {self.customer.name}"
