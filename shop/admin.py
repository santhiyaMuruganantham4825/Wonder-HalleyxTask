from django.contrib import admin
from django.contrib import admin
from .models import Product, Order
from .models import Category, CustomerProfile

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status', 'trending')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'trending', 'created_at')
    search_fields = ('name',)
    list_filter = ('status', 'trending')



admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomerProfile)

