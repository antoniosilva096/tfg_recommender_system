# recommendations/management/commands/clean_for_demo.py

from django.core.management.base import BaseCommand
from products.models import Product
from recommendations.models import Review
from django.db.models import Count, Q

class Command(BaseCommand):
    help = "Limpia la base de datos dejando solo 2000 productos óptimos para demo"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Iniciando limpieza de la base de datos para la demo...")

        # 1. Selecciona productos con al menos 5 reseñas, imagen y categoría
        productos_buenos = (
            Product.objects
            .filter(
                price__gt=0,
                title__isnull=False,
                image_url__isnull=False,
                image_url__gt='',
                categories__isnull=False,
            )
            .annotate(num_reviews=Count("review"))
            .filter(num_reviews__gte=5)
            .order_by("-average_rating")[:2000]
        )

        ids_a_mantener = list(productos_buenos.values_list("id", flat=True))

        self.stdout.write(f"✅ Productos seleccionados: {len(ids_a_mantener)}")

        # 2. Eliminar reviews y productos que no estén en el top 2000
        productos_total = Product.objects.count()
        reviews_total = Review.objects.count()

        Review.objects.exclude(product_id__in=ids_a_mantener).delete()
        Product.objects.exclude(id__in=ids_a_mantener).delete()

        self.stdout.write(f"🧹 Reviews eliminadas: {reviews_total - Review.objects.count()}")
        self.stdout.write(f"🧹 Productos eliminados: {productos_total - Product.objects.count()}")

        # 3. Opcional: eliminar categorías huérfanas
        from products.models import Category
        cat_eliminadas = Category.objects.annotate(n=Count("products")).filter(n=0).delete()

        self.stdout.write(f"🗑️ Categorías sin productos eliminadas: {cat_eliminadas[0]}")

        self.stdout.write(self.style.SUCCESS("🎯 Limpieza completada con éxito."))
