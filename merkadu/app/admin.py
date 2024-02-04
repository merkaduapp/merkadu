from django.contrib import admin
from .models import Market, Product, Order, BaseConfiguration, CustomUser, CustomUser, ProdutoCatalogo
from django.contrib.auth.admin import UserAdmin


class BaseConfigurationAdmin(admin.ModelAdmin):
    pass


class MarketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'delivery_fee', 'min_order_value', 'is_active']
    search_fields = ['name', 'user__email', 'cnpj', 'phone_number']

class ProductCatalogAdmin(admin.ModelAdmin):
    list_display = ["category", "name", "description", "value", "image"]
    list_filter = ('category',)
    search_fields = [
"category", 'name', 'description']

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "name", "descript", "value", "offer_value", "quantity_in_stock", "image", "is_active", "created_at", "updated_at"]
    list_filter = ('name',)
    search_fields = [
"category", 'name', 'descript']


class OrderAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProdutoCatalogo, ProductCatalogAdmin)
admin.site.register(Market, MarketAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BaseConfiguration, BaseConfigurationAdmin)