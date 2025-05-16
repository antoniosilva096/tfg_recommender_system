import numpy as np

from products.models import Product
from recommendations.models import Review
from recommendations.utils import build_user_item_matrix


def item_based_collaborative(user_id, top_k=5):
    # 1) Construir la matriz
    matrix, user_ids, product_ids = build_user_item_matrix()

    # 2) Ubicar el índice del usuario
    if user_id not in user_ids:
        return []  # usuario no tiene reseñas, no podemos recomendar

    user_idx = user_ids.index(user_id)

    # 3) Calcular similitud entre productos (matriz de item-based)
    product_vectors = matrix.T  # shape: [num_products x num_users]
    norms = np.linalg.norm(product_vectors, axis=1, keepdims=True)
    product_vectors_normed = product_vectors / (norms + 1e-9)
    similarity_matrix = np.dot(product_vectors_normed, product_vectors_normed.T)

    # 4) Puntajes para productos según las reseñas del usuario
    user_ratings = matrix[user_idx]  # vector con las calificaciones del usuario
    scores = np.dot(similarity_matrix, user_ratings)

    # 5) Evitar recomendar lo que ya ha reseñado
    already_interacted = np.where(user_ratings > 0)[0]
    scores[already_interacted] = -np.inf

    # 6) Tomar el top_k
    top_indices = np.argsort(scores)[::-1][:top_k]
    recommended_product_ids = [product_ids[i] for i in top_indices]

    return recommended_product_ids




import numpy as np
from django.db.models import Count
from random import sample
from products.models import Product
from recommendations.models import Review

def recommend_similar_products(product_id, top_n=4):
    """
    Recomienda productos similares a un producto dado, usando
    filtrado colaborativo item-item basado en ratings de usuarios,
    evitando excesivo consumo de memoria.
    """
    # 1) Obtener reviews
    reviews = Review.objects.all()
    if not reviews.exists():
        return []

    # 2) Seleccionar productos con más reviews (TOP 500)
    top_products_qs = (
        Review.objects.values('product_id')
        .annotate(total=Count('id'))
        .order_by('-total')[:500]
    )
    product_ids = [item['product_id'] for item in top_products_qs]

    # 3) Seleccionar usuarios aleatorios (máx 1000)
    all_user_ids = list(Review.objects.values_list('user_id', flat=True).distinct())
    user_ids = sample(all_user_ids, min(1000, len(all_user_ids)))

    # 4) Índices
    product_index = {pid: idx for idx, pid in enumerate(product_ids)}
    index_product = {idx: pid for pid, idx in product_index.items()}
    user_index = {uid: idx for idx, uid in enumerate(user_ids)}

    # 5) Matriz vacía
    matrix = np.zeros((len(product_ids), len(user_ids)))

    for r in reviews.filter(product_id__in=product_ids, user_id__in=user_ids):
        i = product_index.get(r.product_id)
        j = user_index.get(r.user_id)
        if i is not None and j is not None:
            matrix[i][j] = r.rating

    # 6) Verificar existencia del producto en el set reducido
    if product_id not in product_index:
        print("⚠️ Producto no está entre los top 500 con más reviews.")
        return list(Product.objects.exclude(id=product_id).values_list('id', flat=True)[:top_n])

    # 7) Vector del producto y cálculo de similitud coseno
    target_vector = matrix[product_index[product_id]]

    def cosine_similarity(a, b):
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    similarities = []
    for idx in range(len(product_ids)):
        if product_ids[idx] == product_id:
            continue
        sim = cosine_similarity(target_vector, matrix[idx])
        similarities.append((product_ids[idx], sim))

    # 8) Ordenar y devolver
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar = [pid for pid, sim in similarities[:top_n]]

    print("🎯 Total productos usados:", len(product_ids))
    print("👤 Usuarios analizados:", len(user_ids))
    print("📥 Producto objetivo:", product_id)
    print("📊 Similitudes:", similarities[:top_n])
    print("🧠 Resultados:", top_similar)

    if not top_similar:
        print("⚠️ No se encontraron similares. Se devuelven aleatorios.")
        return list(Product.objects.exclude(id=product_id).values_list('id', flat=True)[:top_n])

    return top_similar
