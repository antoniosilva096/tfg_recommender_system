from django.contrib import admin
from .models import Review, RecommendationEvaluation

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'rating',
        'short_review_text',
        'created_at'
    )
    list_filter = ('rating', 'user', 'product')
    search_fields = ('user__username', 'product__asin', 'product__title', 'review_text')
    ordering = ('-created_at',)
    autocomplete_fields = ['user', 'product']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'product')

    def short_review_text(self, obj):
        if obj.review_text:
            return (obj.review_text[:40] + '...') if len(obj.review_text) > 40 else obj.review_text
        return ''
    short_review_text.short_description = "Extracto Review"


@admin.register(RecommendationEvaluation)
class RecommendationEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'algorithm',
        'metric',
        'formatted_k_value',
        'value',
        'timestamp'
    )
    list_filter = ('algorithm', 'metric')
    search_fields = ('algorithm', 'metric')
    ordering = ('-timestamp',)

    def formatted_k_value(self, obj):
        return f"@{obj.k_value}" if obj.k_value else "-"
    formatted_k_value.short_description = "K"
