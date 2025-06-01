# recommendations/management/commands/clean_for_demo.py

from django.core.management.base import BaseCommand
from products.models import Product, Category
from recommendations.models import Review
from django.db.models import Count, Q

class Command(BaseCommand):
    help = "Limpia la base de datos dejando solo los 5000 productos más óptimos para demo o entrenamiento"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra lo que se eliminaría sin aplicar cambios'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        self.stdout.write("🚀 Iniciando limpieza de la base de datos para demo/entrenamiento...")

        # Productos con buena calidad de datos
        productos_buenos = (
            Product.objects
            .filter(
                price__gte=5,
                price__lte=1000,
                title__isnull=False,
                image_url__isnull=False,
                image_url__gt='',
                categories__isnull=False
            )
            .annotate(
                num_reviews=Count("review"),
                num_cats=Count("categories")
            )
            .filter(
                num_reviews__gte=5,
                num_cats__gte=1,
                title__length__gte=15
            )
            .order_by("-average_rating")[:5000]
        )

        ids_a_mantener = list(productos_buenos.values_list("id", flat=True))

        # Contar antes de eliminar
        productos_total = Product.objects.count()
        reviews_total = Review.objects.count()
        categorias_total = Category.objects.count()

        productos_a_eliminar = productos_total - len(ids_a_mantener)
        reviews_a_eliminar = Review.objects.exclude(product_id__in=ids_a_mantener).count()

        self.stdout.write(f"🧠 Productos seleccionados: {len(ids_a_mantener)} de {productos_total}")
        self.stdout.write(f"🧠 Reviews a eliminar: {reviews_a_eliminar}")
        self.stdout.write(f"🧠 Productos a eliminar: {productos_a_eliminar}")

        if dry_run:
            self.stdout.write(self.style.WARNING("⚠️ Simulación activa (dry-run). No se aplicaron cambios."))
            return

        # Eliminación real
        Review.objects.exclude(product_id__in=ids_a_mantener).delete()
        Product.objects.exclude(id__in=ids_a_mantener).delete()

        # Limpieza de categorías sin productos
        cat_eliminadas = Category.objects.annotate(n=Count("products")).filter(n=0).delete()

        self.stdout.write(f"🗑️ Categorías eliminadas: {cat_eliminadas[0]}")
        self.stdout.write(self.style.SUCCESS("✅ Limpieza completada con éxito."))
