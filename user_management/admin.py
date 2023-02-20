from django.contrib import admin
from .models import *
# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', "address_type", "city", "state", "phone_number"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "contact_number"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "order_id", "payment_status", "discount", "subtotal", "total"]


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "discount", "subtotal", "total"]


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
