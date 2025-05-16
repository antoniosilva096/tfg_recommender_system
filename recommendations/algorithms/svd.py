import pickle
from surprise import SVD
from recommendations.models import Review
from products.models import Product
import os

MODEL_PATH = "svd_model.pkl"

def svd_recommendations(user_id, top_n=4):
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Modelo SVD no entrenado aún.")
        return []

    with open(MODEL_PATH, "rb") as f:
        model: SVD = pickle.load(f)

    # Tomar todos los productos
    productos = Product.objects.all()

    # Excluir los ya calificados
    vistos = Review.objects.filter(user_id=user_id).values_list("product_id", flat=True)

    predicciones = []
    for producto in productos:
        if producto.id in vistos:
            continue
        est = model.predict(str(user_id), str(producto.id))
        predicciones.append((producto.id, est.est))

    # Ordenar por score
    predicciones.sort(key=lambda x: x[1], reverse=True)
    return [pid for pid, _ in predicciones[:top_n]]
