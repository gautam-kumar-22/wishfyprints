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

urlpatterns = [
    path('', views.home, name='home'),
    path('services', views.services, name='services'),
    path('about-us', views.about, name='about-us'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('faq', views.faq, name='faq'),
    path('service-detail/<slug>', views.service_details, name='service-detail'),
    path('products', views.products, name='products'),
    path('product-details/<slug>', views.product_details, name='product-details'),
    path('contact-us', views.contact_us, name='contact-us'),

]
