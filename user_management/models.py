from django.db import models
from django.contrib.auth.models import User
from prints.models import Product, TimeStampedModel
import datetime
from decimal import Decimal


class Address(models.Model):
    ADDRESS_TYPE = (
        ('shipping', 'Shipping Address'),
        ('billing', 'Billing Address'),
        ('order_shipping', 'Order Shipping Address'),
        ('order_billing', 'Order Billing Address')
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=False, blank=False, default="")
    last_name = models.CharField(max_length=50, null=False, blank=False, default="")
    address_type = models.CharField(choices=ADDRESS_TYPE, default='shipping', max_length=20)
    is_billing_address_same_as_shipping = models.BooleanField(default=True)
    primary_address = models.CharField(max_length=255, null=False, blank=False)
    primary_address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False, default="India")
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    pin_code = models.CharField(max_length=10, null=False, blank=False)
    landmark = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}: Address Type: {self.address_type}, City: {self.city}, State: {self.state}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    image = models.FileField(upload_to='Media/user', blank=True, null=True, default='Media/default.jpg')
    contact_number = models.CharField(max_length=15, null=False, blank=False, default="+91 0000000000")

    def __str__(self):
        return self.user.first_name


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}-{self.product.title}-Quantity: {self.quantity}"


class Wishlist(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}-{self.product.title}"


def increment_order_id():
    """ Creates Order ID of format  ABCD  . Change as per neeed."""
    prefix = 'WISH'
    last_order = Order.objects.all().order_by('id').last()
    if not last_order:
        return str(prefix) + str(datetime.date.today().year) + str(
            datetime.date.today().month).zfill(2) + str(
            datetime.date.today().day).zfill(2) + '0000'
    order_id = last_order.order_id
    order_id_int = int(order_id[12:16])
    new_order_id_int = order_id_int + 1
    new_order_id = str(prefix) + str(str(datetime.date.today().year)) + str(
      datetime.date.today().month).zfill(2) + str(
      datetime.date.today().day).zfill(2) + str(new_order_id_int).zfill(4)
    return new_order_id


class Order(TimeStampedModel):
    """ Order Model """
    NOTPAID = 0
    PAID = 1
    PARTPAID = 2
    CANCELLED = 3

    PAYMENT_STATUS = (
        (NOTPAID, 'Not Paid'),
        (PARTPAID, 'Partial Paid'),
        (PAID, 'Paid'),
        (CANCELLED, 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    order_id = models.CharField(max_length=20, default=increment_order_id, null=True, blank=True, editable=False)
    stripe_payment_intent = models.CharField(max_length=200, null=True)
    payment_status = models.IntegerField(default=NOTPAID, choices=PAYMENT_STATUS, null=False)
    lock = models.BooleanField(default=False, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ('-created_on', '-id')

    def __str__(self):
        return '%s' % (self.order_id)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='orderitems', null=True)
    desc = models.CharField(max_length=500, null=True)
    stripe_payment_intent = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1, null=False)
    tax = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Records
    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.id)

    def description(self):
        # If items is linked, return item's description
        if self.item:
          return str(self.item.name)
        else:
          return 'Order Item'

    class Meta:
        get_latest_by = 'created'
        ordering = ('-created',)


class UserOrderAddress(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)


class Review(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=5)
    status = models.BooleanField(default=True)
