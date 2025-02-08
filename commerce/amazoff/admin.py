from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(people)
admin.site.register(address)
admin.site.register(orders)
admin.site.register(company)
admin.site.register(product)
admin.site.register(inventory)
admin.site.register(review)
admin.site.register(orderdetails)
admin.site.register(cart)
admin.site.register(cartitems)