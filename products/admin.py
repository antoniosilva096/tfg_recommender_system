from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'asin', 
        'title', 
        'image_preview',   # Miniatura de la imagen
        'price', 
        'average_rating', 
        'get_categories'
    )
    list_filter = ('price', 'average_rating', 'categories')
    search_fields = ('asin', 'title')
    filter_horizontal = ('categories',)
    ordering = ('title',)
    list_editable = ('price', 'average_rating')
    readonly_fields = ('image_preview',)

    def get_queryset(self, request):
        # Optimiza la consulta, especialmente con ManyToMany
        qs = super().get_queryset(request)
        return qs.prefetch_related('categories')

    def get_categories(self, obj):
        """Muestra las categorías separadas por comas."""
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = "Categorías"

    def image_preview(self, obj):
        """Previsualización de la imagen del producto en el admin."""
        if obj.image_url:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.image_url)
        return "Sin imagen"
    image_preview.short_description = "Imagen"

    # Acción personalizada
    actions = ['reset_rating']

    def reset_rating(self, request, queryset):
        updated = queryset.update(average_rating=0)
        self.message_user(request, f"Se han actualizado {updated} productos (rating = 0).")
    reset_rating.short_description = "Poner rating a 0"

