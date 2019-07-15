from django.contrib import admin

# Register your models here.
from inventory.models import Product, OutputMovement

admin.site.register(Product)
admin.site.register(OutputMovement)
