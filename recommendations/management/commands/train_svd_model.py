import pickle
import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from django.core.management.base import BaseCommand
from recommendations.models import Review

class Command(BaseCommand):
    help = "Entrena un modelo SVD y lo guarda en disco"

    def handle(self, *args, **options):
        print("🧠 Extrayendo reseñas de la base de datos...")
        data = []
        for r in Review.objects.all():
            data.append((str(r.user_id), str(r.product_id), float(r.rating)))

        if not data:
            print("❌ No hay reseñas suficientes.")
            return

        reader = Reader(rating_scale=(0.5, 5.0))
        dataset = Dataset.load_from_df(
            pd.DataFrame(data, columns=["userID", "itemID", "rating"]),
            reader
        )

        print("📚 Entrenando modelo SVD...")
        trainset = dataset.build_full_trainset()
        model = SVD()
        model.fit(trainset)

        print("💾 Guardando modelo en disk: svd_model.pkl")
        with open("svd_model.pkl", "wb") as f:
            pickle.dump(model, f)

        print("✅ Modelo SVD entrenado y guardado.")
