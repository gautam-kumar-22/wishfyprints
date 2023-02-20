from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from user_management.models import Cart, Review


def get_page_context(request):
    menus = Menu.objects.filter(status=True).order_by('rank')
    submenus = Submenu.objects.filter(status=True)
    setting = Settings.objects.all().first()
    contacts = Contact.objects.all().first()
    categories = Category.objects.filter(status=True)
    carts = 0
    if request.user:
        carts = Cart.objects.filter(user=request.user.id)
    context = {"menus": menus, 'submenus': submenus, "settings": setting, "contacts": contacts,
               "categories": categories, "carts": carts}
    return context


def get_home_page_detail(request):
    about_us = AboutUs.objects.all().first()
    features = Features.objects.filter(status=True)
    service = Service.objects.filter(status=True)
    context = get_page_context(request)
    slider = Slider.objects.filter(page__title='Home')
    projects = Project.objects.filter(status=True)
    products = Product.objects.filter(status=True)
    photos = Photo.objects.all()
    categories = Category.objects.filter(status=True)
    testimonials = Testimonial.objects.all()
    blog = Blog.objects.filter(status=True)
    context.update({
        "services": service,
        "projects": projects,
        "products": products,
        "photos": photos,
        "testimonials": testimonials,
        "blogs": blog,
        "about_us": about_us,
        "features": features,
        "categories": categories,
        "slider": slider
    })
    return context


def save_user_information(request):
    if request.user.username:
        user = request.user
        #  if username exists in database, not save information else save.
        if len(User.objects.filter(username=user.username)):
            #  User already exists
            print(f"User {user.username} already exists.")
        else:
            data = dict()
            data["username"] = user.username
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
            data["email"] = user.email
            data["is_superuser"] = False
            data["is_staff"] = True
            data["is_active"] = True
            User.objects.create(**data)


def home(request):
    context = get_home_page_detail(request)
    return render(request, "home.html", context=context)


def services(request):
    context = get_page_context(request)
    service = Service.objects.filter(status=True)
    context.update({
        "services": service
    })
    return render(request, "services/service.html", context=context)


def about(request):
    context = get_page_context(request)
    about_us = AboutUs.objects.all().first()
    testimonials = Testimonial.objects.filter(status=True)
    context.update({
        "about_us": about_us,
        "testimonials": testimonials
    })
    return render(request, "about/about.html", context=context)


def testimonial(request):
    context = get_page_context(request)
    testimonials = Testimonial.objects.filter(status=True)
    context.update({
        "testimonials": testimonials
    })
    return render(request, "about/testimonial.html", context=context)


def faq(request):
    context = get_page_context(request)
    faqs = Faq.objects.filter(status=True)
    context.update({
        "faqs": faqs
    })
    return render(request, "about/faq.html", context=context)


def service_details(request, slug):
    context = get_page_context(request)
    service = Service.objects.filter(status=True)
    service_detail = get_object_or_404(Service, slug__iexact=slug)
    context.update({
        "services": service,
        "service_details": service_detail
    })
    return render(request, "services/service-details.html", context=context)


def products(request):
    product_list = Product.objects.filter(status=True).order_by('-id')
    context = get_page_context(request)
    categories = Category.objects.filter(status=True)
    category = request.GET.get('category', "").lower()
    if category and category != "all":
        try:
            product_list = product_list.filter(category__type=category)
        except Exception as e:
            pass
    sortby = request.GET.get('sortby', "").lower()
    orderby = request.GET.get('orderby', "").lower()
    if sortby and orderby:
        if orderby == "asc" and sortby == "name":
            product_list = product_list.order_by("title")
        if orderby == "desc" and sortby == "name":
            product_list = product_list.order_by("-title")
        if orderby == "asc" and sortby == "price":
            product_list = product_list.order_by("price")
        if orderby == "desc" and sortby == "price":
            product_list = product_list.order_by("-price")
    context.update({
        "products": product_list,
        "categories": categories
    })
    return render(request, "product/products.html", context=context)


def product_details(request, slug):
    context = get_page_context(request)
    product_detail = get_object_or_404(Product, slug__iexact=slug)
    products = Product.objects.filter(status=True, category=product_detail.category)
    reviews = Review.objects.filter(product=product_detail.id)
    context.update({
        "similar_products": products,
        "product_details": product_detail,
        "reviews": reviews
    })
    return render(request, "product/product-details.html", context=context)


def contact_us(request):
    context = get_page_context(request)
    if request.method == "POST":
        data = {
            "name": request.POST.get("name", ""),
            "email": request.POST.get("email", ""),
            "subject": request.POST.get("subject", ""),
            "message": request.POST.get("message", ""),
        }
        ContactUs.objects.create(**data)
        messages.success(request, "Success: Thank you for connecting to us. Our team will contact you soon.")
        redirect(request.headers.get('Referer'))
    return render(request, "contact/contact.html", context=context)
