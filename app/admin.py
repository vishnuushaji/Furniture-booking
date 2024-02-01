from django.contrib import admin
from .models import Product,Cart

admin.site.register(Product)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_products_list']

    def get_products_list(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])

    get_products_list.short_description = 'Products in Cart'

admin.site.register(Cart, CartAdmin)
