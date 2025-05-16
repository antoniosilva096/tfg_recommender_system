import numpy as np
from recommendations.models import Review

def build_user_item_matrix():
    # Extraer todas las reseñas
    reviews = Review.objects.select_related("user", "product")

    # Listas únicas de usuarios y productos
    user_ids = list(set(r.user_id for r in reviews))  # user_id es la FK real (un entero)
    product_ids = list(set(r.product_id for r in reviews))

    user_to_index = {u: i for i, u in enumerate(user_ids)}
    product_to_index = {p: j for j, p in enumerate(product_ids)}

    matrix = np.zeros((len(user_ids), len(product_ids)))

    for r in reviews:
        u_idx = user_to_index[r.user_id]
        p_idx = product_to_index[r.product_id]
        matrix[u_idx, p_idx] = r.rating or 0.0

    return matrix, user_ids, product_ids
