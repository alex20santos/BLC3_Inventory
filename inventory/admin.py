from django.contrib import admin

# Register your models here.
from inventory.models import Product, OutputMovement, InputMovement

admin.site.register(Product)
admin.site.register(OutputMovement)
admin.site.register(InputMovement)
