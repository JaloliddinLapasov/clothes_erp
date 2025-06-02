from django.contrib import admin
from .models import Category, Product, Customer, Sale, SaleItem, Income


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'size', 'color', 'is_active']
    list_filter = ['category', 'size', 'color', 'is_active', 'created_at']
    search_fields = ['name', 'brand']
    list_editable = ['price', 'stock_quantity', 'is_active']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'city', 'created_at', 'is_active']
    list_filter = ['gender', 'city', 'is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['is_active']


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_amount', 'payment_method', 'sale_date']
    list_filter = ['payment_method', 'sale_date']
    search_fields = ['customer__first_name', 'customer__last_name']
    inlines = [SaleItemInline]


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'income_type', 'date']
    list_filter = ['income_type', 'date']
    search_fields = ['title']