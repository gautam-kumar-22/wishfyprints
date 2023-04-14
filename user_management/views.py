from prints.views import get_page_context
from .models import Address, UserProfile, Cart, Wishlist, UserOrderAddress, Order, OrderItems, Review
from prints.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AddressForm, PaypalFormView
from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
import stripe
import logging
import json


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def login(request):
    context = get_page_context(request)
    return render(request, "user/login.html", context=context)


@login_required
def add_to_cart(request, id):
    try:
        product = Product.objects.get(pk=int(id))
        product_in_cart = Cart.objects.filter(user=request.user, product=product)
        cart_product = product_in_cart.first()
        if len(product_in_cart):
            if cart_product.quantity < 10:
                cart_product.quantity = cart_product.quantity + 1
                cart_product.save()
        else:
            Cart.objects.create(user=request.user, product=product)
        messages.success(request, "Success: Your cart has been updated..")
    except Product.DoesNotExist as err:
        print(f"Product doesn't exists for id {id}")
        logging.log(1, f"Product doesn't exists for id {id}")
    return redirect("/cart")


@login_required
def delete_cart(request, pk):
    if pk:
        Cart.objects.filter(pk=pk).delete()
        messages.success(request, "Success: Item has been removed from cart.")
    return redirect("/cart")


@login_required
def delete_wishlist(request, pk):
    if pk:
        Wishlist.objects.filter(pk=pk).delete()
        messages.success(request, "Success: Item has been removed from wishlist.")
    return redirect("/wishlists")


@login_required
def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(pk=int(product_id))
        product_in_wishlist = Wishlist.objects.filter(user=request.user, product=product)
        if not len(product_in_wishlist):
            Wishlist.objects.create(user=request.user, product=product)
    except Product.DoesNotExist as err:
        print(f"Product doesn't exists for id {product_id}")
        logging.log(1, f"Product doesn't exists for id {product_id}")
    # return redirect(request.headers.get('Referer'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def wishlist(request):
    context = get_page_context(request)
    wishlists = Wishlist.objects.filter(user=request.user)
    context.update(({"wishlists": wishlists}))
    return render(request, "user/wishlist.html", context=context)


@login_required
def add_to_carts(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id', 0))
        quantity = int(request.POST.get('quantity', 0))
        if quantity <= 0:
            Cart.objects.filter(id=product_id).delete()
            return redirect("/cart")
        if quantity > 10:
            return redirect("/cart")
        try:
            product = Product.objects.get(pk=int(product_id))
            product_in_cart = Cart.objects.filter(user=request.user, product=product)
            if len(product_in_cart):
                cart_product = product_in_cart.first()
                cart_product.quantity = quantity
                cart_product.save()
            else:
                Cart.objects.create(user=request.user, product=product, quantity=quantity)
            messages.success(request, "Success: Cart item has been updated..")
        except Product.DoesNotExist as err:
            print(f"Product doesn't exists for id {id}")
            logging.log(1, f"Product doesn't exists for id {id}")

    return redirect("/cart")


@login_required
def cart(request):
    context = get_page_context(request)
    carts = Cart.objects.filter(user=request.user)
    context.update(({"carts": carts}))
    return render(request, "user/cart.html", context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            # htmly = get_template('user/Email.html')
            # d = {'username': username}
            # subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            # html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title': 'register here'})


def reset_password(request):
    context = get_page_context(request)
    return render(request, "user/reset-password.html", context=context)


@login_required
def profile(request):
    context = get_page_context(request)
    user = User.objects.get(username=request.user.username)
    user_contact = Address.objects.filter(user=request.user)
    user_profile = UserProfile.objects.filter(user=request.user)
    shipping_address = Address.objects.filter(user=request.user, address_type="shipping")
    billing_address = Address.objects.filter(user=request.user, address_type="billing")
    context.update({"user": user, "user_contact": user_contact, "user_profile": user_profile,
                    "shipping_address": shipping_address, "billing_address": billing_address})
    return render(request, "user/profile.html", context=context)


@login_required
def edit_profile(request):
    context = get_page_context(request)
    user = User.objects.get(username=request.user.username)
    user_contact = Address.objects.filter(user=request.user)
    user_profile = UserProfile.objects.filter(user=request.user)
    context.update({"user": user, "user_contact": user_contact, "user_profile": user_profile})
    if request.method == "POST":
        first_name = request.POST.get('first_name', "")
        last_name = request.POST.get('last_name', "")
        email = request.POST.get('email', "")
        phone_number = request.POST.get('phone_number', "")
        profile_pic = ""
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES.get('profile_pic')
        if first_name and last_name and email:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
        if phone_number:
            if len(user_contact):
                user_contact = user_profile.first()
                user_contact.contact_number = phone_number
                user_contact.save()
            else:
                UserProfile.objects.create(user=user, contact_number=phone_number)
        if profile_pic:
            if len(user_profile):
                user_profile = user_profile.first()
                user_profile.image = profile_pic
                user_profile.save()
            else:
                UserProfile.objects.create(user=user, image=profile_pic)
        response = redirect('/profile')
        return response
    return render(request, "user/edit_profile.html", context=context)


@login_required
def checkout_process(request):
    context = get_page_context(request)
    user = User.objects.get(username=request.user.username)
    user_contact = Address.objects.filter(user=request.user)
    user_profile = UserProfile.objects.filter(user=request.user)
    shipping_address = Address.objects.filter(user=request.user, address_type="shipping")
    billing_address = Address.objects.filter(user=request.user, address_type="billing")
    carts = Cart.objects.filter(user=request.user)

    if not len(shipping_address) or not len(billing_address):
        messages.error(request, "Error: Your profile is incomplete, please complete it first..")
        return redirect('/edit-address')

    context.update({"user": user, "user_contact": user_contact, "user_profile": user_profile,
                    "shipping_address": shipping_address, "billing_address": billing_address,
                    "carts": carts})
    return render(request, "user/checkout_process.html", context=context)


@login_required
def orders(request):
    context = get_page_context(request)
    return render(request, "user/orders.html", context=context)


@login_required
def edit_address(request):
    context = get_page_context(request)
    user = User.objects.get(username=request.user.username)
    address = Address.objects.filter(user=request.user)
    shipping_address = Address.objects.filter(user=request.user, address_type="shipping")
    billing_address = Address.objects.filter(user=request.user, address_type="billing")
    context.update({"user": user, "address": address, "shipping_address": shipping_address,
                    "billing_address": billing_address})
    if request.method == "POST":
        first_name = request.POST.get('first_name', "")
        last_name = request.POST.get('last_name', "")
        primary_address = request.POST.get('primary_address', "")
        primary_address2 = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zip_code = request.POST.get('pin_code', "")
        landmark = request.POST.get('landmark', "")
        phone_number = request.POST.get('phone_number', "")
        is_billing_same = request.POST.get('is_billing_same', False)
        if not len(shipping_address):
            shipping_address = Address.objects.create(user=request.user)
        else:
            shipping_address = shipping_address.first()

        shipping_address.first_name = first_name
        shipping_address.last_name = last_name
        shipping_address.primary_address = primary_address
        shipping_address.primary_address2 = primary_address2
        shipping_address.city = city
        shipping_address.state = state
        shipping_address.pin_code = zip_code
        shipping_address.landmark = landmark
        shipping_address.phone_number = phone_number
        shipping_address.is_billing_address_same_as_shipping = is_billing_same
        shipping_address.save()

        if not is_billing_same:
            billing_first_name = request.POST.get('billing_first_name', "")
            billing_last_name = request.POST.get('billing_last_name', "")
            billing_primary_address = request.POST.get('billing_primary_address', "")
            billing_primary_address2 = request.POST.get('billing_primary_address2', "")
            billing_city = request.POST.get('billing_city', "")
            billing_state = request.POST.get('billing_state', "")
            billing_pin_code = request.POST.get('billing_pin_code', "")
            billing_landmark = request.POST.get('billing_landmark', "")
            billing_phone_number = request.POST.get('billing_phone_number', "")
            if len(billing_address):
                billing_address = billing_address.first()
            else:
                billing_address = Address.objects.create(user=request.user, address_type="billing")
            billing_address.first_name = billing_first_name
            billing_address.last_name = billing_last_name
            billing_address.primary_address = billing_primary_address
            billing_address.primary_address2 = billing_primary_address2
            billing_address.city = billing_city
            billing_address.state = billing_state
            billing_address.pin_code = billing_pin_code
            billing_address.landmark = billing_landmark
            billing_address.phone_number = billing_phone_number
            billing_address.save()
        else:
            billing_address = Address.objects.filter(user=request.user, address_type="billing")
            if len(billing_address):
                billing_address = billing_address.first()
            else:
                billing_address = Address.objects.create(user=request.user, address_type="billing")
            billing_address.first_name = first_name
            billing_address.last_name = last_name
            billing_address.primary_address = primary_address
            billing_address.primary_address2 = primary_address2
            billing_address.city = city
            billing_address.state = state
            billing_address.pin_code = zip_code
            billing_address.landmark = landmark
            billing_address.phone_number = phone_number
            billing_address.save()

        return redirect('/profile')
    return render(request, "user/edit_address.html", context=context)


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "user/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(Order, stripe_payment_intent=session.stripe_id)
        order.payment_status = 1
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(LoginRequiredMixin, TemplateView):
    template_name = "user/payment_failed.html"


class OrderHistoryListView(LoginRequiredMixin, ListView):
    template_name = "user/order_list.html"

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        context = get_page_context(request)
        context.update({"orders": orders})
        return render(request, self.template_name, context=context)


def payment_process(request):
    if request.method == "POST":
        user = request.user
        # Billing Address Management
        billing_first_name = request.POST.get('billing_first_name')
        billing_last_name = request.POST.get('billing_last_name')
        billing_primary_address = request.POST.get('billing_primary_address')
        billing_primary_address2 = request.POST.get('billing_primary_address2')
        billing_city = request.POST.get('billing_city')
        billing_state = request.POST.get('billing_state')
        billing_zip = request.POST.get('billing_zip')
        billing_phone_number = request.POST.get('billing_phone_number')
        billing_landmark = request.POST.get('billing_landmark')
        billing_address = Address.objects.create(user=user, first_name=billing_first_name, last_name=billing_last_name,
                                                 primary_address=billing_primary_address,
                                                 primary_address2=billing_primary_address2,
                                                 city=billing_city, state=billing_state, pin_code=billing_zip,
                                                 phone_number=billing_phone_number, landmark=billing_landmark,
                                                 address_type="order_billing")

        # Shipping Address Management
        shipping_first_name = request.POST.get('shipping_first_name')
        shipping_last_name = request.POST.get('shipping_last_name')
        shipping_primary_address = request.POST.get('shipping_primary_address')
        shipping_primary_address2 = request.POST.get('shipping_primary_address2')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_zip = request.POST.get('shipping_zip')
        shipping_phone_number = request.POST.get('shipping_phone_number')
        shipping_landmark = request.POST.get('shipping_landmark')
        shipping_address = Address.objects.create(user=user, first_name=shipping_first_name,
                                                  last_name=shipping_last_name,
                                                  primary_address=shipping_primary_address,
                                                  primary_address2=shipping_primary_address2,
                                                  city=shipping_city, state=shipping_state, pin_code=shipping_zip,
                                                  phone_number=shipping_phone_number, landmark=shipping_landmark,
                                                  address_type="order_shipping")

        validation = [billing_first_name, billing_last_name, billing_primary_address, billing_city, billing_state,
                        billing_zip, billing_phone_number, billing_landmark, shipping_first_name, shipping_last_name,
                        shipping_primary_address, shipping_city, shipping_state, shipping_zip, shipping_phone_number,
                        shipping_landmark]
        if any(len(x) == 0 for x in validation):
            messages.error(request, "Error: Your profile is incomplete, please complete first..")
            context = {}
            return redirect(request.headers.get('Referer'))

        # Create Order
        payment_status = 0  # Not Paid
        total_discount = 0.00
        subtotal = 0.00
        carts = Cart.objects.filter(user=user)
        for items in carts:
            total_discount += (items.product.price * items.product.category.discount / 100) * items.quantity
            subtotal += (items.product.price * items.quantity)
        total = subtotal - total_discount
        order = Order.objects.create(user=user, payment_status=payment_status, discount=total_discount,
                                     subtotal=subtotal, total=total)

        # Save User Order Address Information
        if not len(UserOrderAddress.objects.filter(order=order, address=billing_address)):
            UserOrderAddress.objects.create(user=user, order=order, address=billing_address)
        if not len(UserOrderAddress.objects.filter(order=order, address=shipping_address)):
            UserOrderAddress.objects.create(user=user, order=order, address=shipping_address)

        context = {"stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY, "order": order, "user": request.user}
        return render(request, "user/payment-process.html", context=context)


@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    user = request.user
    stripe.api_key = settings.STRIPE_SECRET_KEY
    carts = Cart.objects.filter(user=user)
    list_items = []
    for items in carts:
        list_items.append({
            'price_data': {
                'currency': 'INR',
                'product_data': {
                    'name': items.product.title,
                },
                'unit_amount': int(
                    items.product.price - (items.product.price * items.product.category.discount / 100)) * 100,
            },
            'quantity': items.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email=user.email,
        payment_method_types=['card'],
        line_items=list_items,
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )
    try:
        order = Order.objects.get(pk=id)
        order.stripe_payment_intent = checkout_session.stripe_id
        order.save()
    except Order.DoesNotExist as err:
        logging.log(1, f"Order doesn't exists for id {id}")

    # Storing data to order-items
    order = Order.objects.get(pk=id)
    for items in carts:
        data = {
            "order": order,
            "stripe_payment_intent": checkout_session.stripe_id,
            "product": items.product,
            "price": items.product.price,
            "quantity": items.quantity,
            "discount": (items.product.price * items.product.category.discount / 100),
            "subtotal": items.product.price * items.quantity,
            "total": (items.product.price - (
                        items.product.price * items.product.category.discount / 100)) * items.quantity,
            "total_discount": (items.product.price * items.product.category.discount / 100) * items.quantity,
        }
        OrderItems.objects.create(**data)

    return JsonResponse({'sessionId': checkout_session.id})


class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "user/order_success.html"

    def get(self, request):
        context = get_page_context(request)
        Cart.objects.filter(user=request.user).delete()
        return render(request, self.template_name, context=context)


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = "user/order_detail.html"

    def get(self, request, id):
        context = get_page_context(request)
        order_detail = Order.objects.filter(pk=id, user=request.user)
        order_billing_address = UserOrderAddress.objects.filter(order=id, user=request.user,
                                                                address__address_type="order_billing")
        order_shipping_address = UserOrderAddress.objects.filter(order=id, user=request.user,
                                                                 address__address_type="order_shipping")
        order_items = OrderItems.objects.filter(order=id, order__user=request.user)
        context.update({"order_details": order_detail, "order_billing_address": order_billing_address,
                        "order_items": order_items, "order_shipping_address": order_shipping_address})
        return render(request, self.template_name, context=context)


def product_review(request):
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comments')
        product_id = request.POST.get('product_id')
        if rating and comment and product_id:
            try:
                product = Product.objects.get(pk=product_id)
                # if not len(Review.objects.filter(user=request.user, product=product, comment=comment)):
                Review.objects.create(user=request.user, product=product, comment=comment, rating=rating)
            except Product.DoesNotExist as err:
                return JsonResponse({"message": f"Product not exists for id {product_id}"})
            return JsonResponse({"message": "Thank you for your comment."})
        return JsonResponse({"message": "Something went wrong, please try again."})
