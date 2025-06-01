from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'product', 
        'rating', 
        'short_review_text', 
        'review_date'
    )
    list_filter = ('rating', 'user', 'product')
    search_fields = ('user__username', 'product__name', 'review_text')
    ordering = ('-review_date',)
    autocomplete_fields = ['user', 'product']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'product')

    def short_review_text(self, obj):
        if obj.review_text:
            return (obj.review_text[:40] + '...') if len(obj.review_text) > 40 else obj.review_text
        return ''
    short_review_text.short_description = "Extracto Review"
