"""company URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path('edit-profile', views.edit_profile, name="edit-profile"),
    path('edit-address', views.edit_address, name="edit-address"),
    path('orders', views.orders, name="orders"),
    path('cart', views.cart, name="cart"),
    path('delete-cart/<pk>', views.delete_cart, name="delete-cart"),
    path('wishlists', views.wishlist, name="wishlists"),
    path('delete-wishlists/<pk>', views.delete_wishlist, name="delete-wishlists"),
    path('add_to_carts', views.add_to_carts, name="add-to-carts"),
    path('add-to-wishlist/<product_id>', views.add_to_wishlist, name="add-to-wishlist"),
    path('add_to_cart/<id>', views.add_to_cart, name="add-to-cart"),
    path('reset-password', views.reset_password, name="reset-password"),
    path('checkout_process', views.checkout_process, name="checkout-process"),
    # Adding social auth path
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Stripe Payment Gateway
    path('success', PaymentSuccessView.as_view(), name='success'),
    path('order-success', OrderSuccessView.as_view(), name='order-success'),
    path('failed', PaymentFailedView.as_view(), name='failed'),
    path('order-history', OrderHistoryListView.as_view(), name='order-history'),
    path('payment-process', views.payment_process, name="payment-process"),
    path('checkout-session/<id>', create_checkout_session, name='checkout-session'),
    path('order-detail/<id>', OrderDetailView.as_view(), name='order-detail'),
    path('product-review', views.product_review, name="product-review")
]
