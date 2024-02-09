from django import template
register = template.Library()

# for check the color is already Selected or not while update the product
@register.filter('checkColor')
def checkColor(color , item):
    value = False
    for i in color.split(","):
        if(i==item):
            value = True
            break
    return value

@register.filter('checkSize')
def checkSize(size , item):
    value = False
    for i in size.split(","):
        if(i==item):
            value = True
            break
    return value

