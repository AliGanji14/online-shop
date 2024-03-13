from django.db import models
from django.conf import settings

from products.models import Product
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    is_paid = models.BooleanField(_('is paid?'), default=False)

    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    phone_number = models.CharField(_('phone number'), max_length=11)
    address = models.CharField(_('address'), max_length=700)

    order_note = models.CharField(_('order notes'), max_length=700, blank=True)

    datetime_created = models.DateTimeField(_('created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('modified'), auto_now=True)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} * {self.quantity} (price:{self.price})'
