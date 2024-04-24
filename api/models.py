from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stocks'


class Order(models.Model):
    ORDER_TYPES = (
        ('BUY', 'BUY'),
        ('SELL', 'SELL')
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'orders'
