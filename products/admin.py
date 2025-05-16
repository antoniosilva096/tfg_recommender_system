from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'price', 'average_rating', 'get_categories')
    list_filter = ('price', 'average_rating', 'categories')
    search_fields = ('asin', 'title')
    filter_horizontal = ('categories',)
    ordering = ('title',)

    def get_categories(self, obj):
        """
        Devuelve una cadena con las categorías asociadas separadas por comas.
        """
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = "Categorías"
