from django import template
from MainApp.models import *
register = template.Library()


@register.filter("cartColor")
def CartColor(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        return cart[num][2]
    else:
        return ""

@register.filter("cartSize")
def CartSize(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        return cart[num][3]
    else:
        return ""

@register.filter("cartQty")
def CartQty(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        return cart[num][1]
    else:
        return ""

@register.filter("cartTotal")
def CartTotal(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return cart[num][1]*p.finalprice
    else:
        return ""

@register.filter("cartProductName")
def CartProductName(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.name
    else:
        return ""

@register.filter("cartProductPrice")
def CartProductPrice(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.finalprice
    else:
        return ""

@register.filter("cartProductImage")
def CartProductImage(request,num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.pic1.url
    else:
        return ""