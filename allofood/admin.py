from django.contrib import admin
from .models import Restaurant
from .models import Product

# admins can manipulate restaurants and products
admin.site.register(Restaurant)
admin.site.register(Product)
