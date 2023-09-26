from django.contrib import admin

# Donne accès à l'admon aux (CRUD) Products 
from .models import Product
admin.site.register(Product)