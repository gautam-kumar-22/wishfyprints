from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.filters import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
import datetime
from .models import *
# Register your models here.


class MyDateTimeFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(MyDateTimeFilter, self).__init__(*args, **kwargs)

        now = datetime.datetime.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.

        today = now.date()

        self.links += ((
            (_('Next 7 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
        ))


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', "address_type", "city", "state", "phone_number"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "contact_number"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]
    list_filter = (('created_on', MyDateTimeFilter,),)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]
    list_filter = (('created_on', MyDateTimeFilter,),)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "user", "payment_status", "discount", "subtotal", "total", "order_status", "created_on",
                    "shipping_date", "delivery_date"]
    search_fields = ["user", "order_id"]
    list_filter = (('created_on', MyDateTimeFilter,),)

    def order_status(self, obj):
        """payment_status_dict = {0: "Not Paid", 1: "Paid", 2: "Partial Paid", 3: "Cancelled"}"""
        payment_status = obj.payment_status
        if payment_status == 1 and obj.shipping_date is None:
            return format_html('<span style="color: orange;"><b>New Order<b></span>')
        if payment_status == 1 and obj.shipping_date is not None and obj.delivery_date is None:
            return format_html('<span style="color: yellowgreen;"><b>Order Shipped<b></span>')
        if payment_status == 1 and obj.shipping_date is not None and obj.delivery_date is not None:
            return format_html('<span style="color: green;"><b>Order Delivered<b></span>')


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "user", "quantity", "discount", "subtotal", "total", "payment_status",
                    "order_status", "created"]
    search_fields = ["order__order_id"]
    list_filter = (('created', MyDateTimeFilter,),)

    def payment_status(self, obj):
        """ Payment status detail
            NOTPAID = 0
            PAID = 1
            PARTPAID = 2
            CANCELLED = 3
        """
        payment_status = obj.order.payment_status
        payment_status_dict = {
            0: "<span style='color: red; font-weight: bold;'>Not Paid</span>",
            1: "<span style='color: green; font-weight: bold;'>Paid</span>",
            2: "<span style='color: yellowgreen; font-weight: bold;'>Partial Paid</span>",
            3: "<span style='color: red; font-weight: bold;'>Cancelled</span>"}
        return format_html(payment_status_dict[payment_status])

    def order_status(self, obj):
        """payment_status_dict = {0: "Not Paid", 1: "Paid", 2: "Partial Paid", 3: "Cancelled"}"""
        payment_status = obj.order.payment_status
        if payment_status == 1 and obj.order.shipping_date is None:
            return format_html('<span style="color: orange;"><b>New Order<b></span>')
        if payment_status == 1 and obj.order.shipping_date is not None and obj.order.delivery_date is None:
            return format_html('<span style="color: yellowgreen;"><b>Order Shipped<b></span>')
        if payment_status == 1 and obj.order.shipping_date is not None and obj.order.delivery_date is not None:
            return format_html('<span style="color: green;"><b>Order Delivered<b></span>')

    def user(self, obj):
        return obj.order.user.username


class UserOrderAddressAdmin(admin.ModelAdmin):
    list_display = ["user", "order", "address"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "rating", "status"]


admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(UserOrderAddress, UserOrderAddressAdmin)
admin.site.register(Review, ReviewAdmin)
