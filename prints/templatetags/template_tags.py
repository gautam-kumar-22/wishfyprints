from django import template
from django.utils.safestring import mark_safe, SafeData
from django.template.defaultfilters import stringfilter
from prints.models import Product
import math
register = template.Library()


@register.filter(name='get_price')
def get_price(price, discount):
    """
    Return final price after calculating discount
    """
    return float(price - (price*discount/100))


@register.filter(name="get_image")
def get_image(product):
    return "../" + product.photos.values()[0].get("photo", None)


@register.filter(name="get_photo_from_photos")
def get_photo_from_photos(photos):
    return "../" + photos.get("photo")


@register.filter(name="get_tags")
def get_tags(tags):
    return [tag for tag in tags.split(",")]


@register.filter(name="get_additional_information")
def get_additional_information(additional_information):
    additional_information = additional_information.values()


@register.simple_tag()
def multiply(price, quantity):
    return "%.2f" % (price * quantity)


@register.simple_tag()
def cart_sub_total(carts):
    sub_total = 0.00
    for cart in carts:
        sub_total += (cart.product.price * cart.quantity)
    return "%.2f" % sub_total


@register.simple_tag()
def cart_total_discount(carts):
    total_discount = 0.00
    for cart in carts:
        total_discount += (cart.product.price*cart.product.category.discount/100) * cart.quantity
    return "%.2f" % total_discount


@register.simple_tag()
def cart_total(carts):
    total = 0.00
    for cart in carts:
        total += (cart.product.price - (cart.product.price*cart.product.category.discount/100)) * cart.quantity
    return "%.2f" % total


@register.simple_tag()
def count_product(category):
    if category == "all":
        return len(Product.objects.filter(status=True))
    else:
        return len(Product.objects.filter(status=True, category=category))


@register.filter(name='myrange')
def myrange(x):
    return range(1, x+1)


@register.filter(name='avgrating')
def avgrating(reviews):
    total = 0
    for review in reviews:
        total += review.rating
    try:
        return range(1, math.ceil(total/len(reviews)) + 1)
    except ZeroDivisionError as err:
        return range(0)

