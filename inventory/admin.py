from django.contrib import admin

# Register your models here.
from inventory.models import Product

admin.site.register(Product)
