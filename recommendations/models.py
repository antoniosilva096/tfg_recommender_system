# recommendations/models.py
from django.db import models
from django.conf import settings  # Para referenciar al modelo de usuario
from products.models import Product

class Review(models.Model):
    # Relación con el usuario real de Django
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # Relación con el producto
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    review_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.asin} ({self.rating})"
