import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Product
from recommendations.models import Review
from accounts.models import Account

class Command(BaseCommand):
    help = "Importa reseñas de Amazon y las enlaza con usuarios Django y productos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv_path",
            type=str,
            help="Ruta al CSV con columnas user_id, asin, rating, review_text",
            default="reviews_clean.csv"
        )

    def handle(self, *args, **options):
        csv_path = options["csv_path"]

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"Archivo no encontrado: {csv_path}"))
            return

        self.stdout.write(f"Importando reseñas desde {csv_path}...")
        total_reviews = 0

        with open(csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                amazon_user_id = row.get("user_id", "").strip()
                asin = row.get("asin", "").strip()
                rating_str = row.get("rating", "").strip()
                review_text = (row.get("review_text") or "").strip()

                if not amazon_user_id or not asin:
                    continue

                try:
                    rating = float(rating_str)
                except ValueError:
                    continue

                try:
                    product = Product.objects.get(asin=asin)
                except Product.DoesNotExist:
                    continue

                account = Account.objects.filter(amazon_user_id=amazon_user_id).first()
                if not account:
                    user = User.objects.create_user(
                        username=f"amazon_{amazon_user_id}",
                        email=f"{amazon_user_id}@fake-amazon.com",
                        password=None
                    )
                    user.is_active = False
                    user.save()

                    account = Account.objects.create(
                        user=user,
                        amazon_user_id=amazon_user_id
                    )
                    self.stdout.write(f"   > Creado usuario para Amazon ID: {amazon_user_id}")
                else:
                    user = account.user

                Review.objects.create(
                    user=user,
                    product=product,
                    rating=rating,
                    review_text=review_text
                )
                total_reviews += 1

        self.stdout.write(self.style.SUCCESS(f"Importación completada. Reseñas creadas: {total_reviews}"))
