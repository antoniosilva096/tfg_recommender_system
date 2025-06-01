from django.utils import timezone
from django.db import models
from django.conf import settings  # Para referenciar al modelo de usuario
from products.models import Product

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    review_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.asin} ({self.rating})"



class RecommendationEvaluation(models.Model):
    ALGORITHM_CHOICES = [
        ('collaborative', 'Filtrado Colaborativo'),
        ('content', 'Content-Based'),
        ('svd', 'SVD Matrix Factorization'),
        ('knn', 'K-Nearest Neighbors'),
        ('hybrid', 'Híbrido'),
    ]

    METRIC_CHOICES = [
        ('rmse', 'RMSE'),
        ('mae', 'MAE'),
        ('precision', 'Precision@K'),
        ('recall', 'Recall@K'),
        ('ctr', 'Click Through Rate'),
        ('avg_cart_value', 'Valor Medio Carrito'),
    ]

    algorithm = models.CharField(max_length=30, choices=ALGORITHM_CHOICES)
    metric = models.CharField(max_length=30, choices=METRIC_CHOICES)
    value = models.FloatField()
    k_value = models.IntegerField(null=True, blank=True)  # Solo útil para métricas @K
    timestamp = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name = "Evaluación de Algoritmo"
        verbose_name_plural = "Evaluaciones de Algoritmos"

    def __str__(self):
        k_suffix = f"@{self.k_value}" if self.k_value else ""
        return f"{self.get_algorithm_display()} - {self.get_metric_display()}{k_suffix}: {self.value:.4f}"