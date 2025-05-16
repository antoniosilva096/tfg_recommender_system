import csv
from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = "Carga productos desde un CSV preprocesado y asocia categorías estandarizadas"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv_path",
            type=str,
            help="Ruta al archivo CSV que contiene los productos",
            default="data/products_clean.csv"  # Ajusta la ruta si es necesario
        )

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        self.stdout.write(f"Cargando productos desde {csv_path}...")
        
        total_nuevos = 0
        with open(csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extraer y limpiar datos básicos
                asin = row.get("asin", "").strip()
                title = row.get("title", "").strip()
                categories_field = row.get("categories", "").strip()
                try:
                    price = float(row.get("price", "0").strip())
                except ValueError:
                    self.stdout.write(f"Error al convertir precio para el producto {title}, se omite.")
                    continue

                try:
                    average_rating = float(row.get("average_rating", "0").strip())
                except ValueError:
                    average_rating = None  # O asigna un valor por defecto

                image_url = row.get("image_url", "").strip()

                # Crear o actualizar el producto
                product, created = Product.objects.get_or_create(
                    asin=asin,
                    defaults={
                        "title": title,
                        "price": price,
                        "average_rating": average_rating,
                        "image_url": image_url,
                    }
                )
                if created:
                    total_nuevos += 1
                    self.stdout.write(f"Producto creado: {title}")
                
                # Procesar las categorías: se asume que están separadas por comas
                cat_names = [cat.strip() for cat in categories_field.split(",") if cat.strip()]
                category_objects = []
                for cat_name in cat_names:
                    category, cat_created = Category.objects.get_or_create(name=cat_name)
                    category_objects.append(category)
                
                # Asignar las categorías al producto (sobrescribe las previas si existen)
                product.categories.set(category_objects)
        
        self.stdout.write(self.style.SUCCESS(f"Carga completada. Total nuevos productos: {total_nuevos}"))
