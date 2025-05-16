import numpy as np
from sklearn.neighbors import NearestNeighbors
from products.models import Product
from recommendations.models import Review

def knn_recommendations(product_id, k=10):
    # Asegurarse de que el producto tiene reseñas
    if not Review.objects.filter(product_id=product_id).exists():
        return [], "❌ Este producto no tiene reseñas."

    # 1. Obtener todos los productos CON reseñas
    product_ids = list(
        Review.objects.values_list("product_id", flat=True)
        .distinct()
    )

    if product_id not in product_ids:
        return [], "❌ Producto no tiene suficientes datos para recomendar."

    # Limitamos a un subconjunto para optimizar memoria
    product_ids = product_ids[:2000]  # <-- AJUSTABLE
    user_ids = list(
        Review.objects.filter(product_id__in=product_ids)
        .values_list("user_id", flat=True)
        .distinct()
    )

    # 2. Crear índices
    product_index = {pid: idx for idx, pid in enumerate(product_ids)}
    user_index = {uid: idx for idx, uid in enumerate(user_ids)}

    # 3. Crear matriz producto-usuario
    matrix = np.zeros((len(product_ids), len(user_ids)))
    for review in Review.objects.filter(product_id__in=product_ids, user_id__in=user_ids):
        i = product_index[review.product_id]
        j = user_index[review.user_id]
        matrix[i][j] = review.rating

    # 4. Comprobamos que no esté todo vacío
    if np.all(matrix == 0):
        return [], "⚠️ No se pudo construir matriz válida de puntuaciones."

    # 5. KNN
    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(matrix)

    distances, indices = model.kneighbors(
        [matrix[product_index[product_id]]],
        n_neighbors=min(k+1, len(product_ids))
    )

    neighbors_idx = indices.flatten()[1:]  # excluir el mismo producto
    recommended_ids = [product_ids[i] for i in neighbors_idx]

    return recommended_ids, None
