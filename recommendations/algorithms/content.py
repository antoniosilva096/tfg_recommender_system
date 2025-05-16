from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from products.models import Product


def content_based_recommendations(product_id, top_n=4):
    """
    Recomienda productos similares en contenido al producto dado.
    Usa TF-IDF sobre título + categorías como texto base.
    """
    # 1) Obtener todos los productos
    productos = list(Product.objects.all())

    if not productos:
        return []

    # 2) Construir corpus textual (título + categorías)
    texts = []
    product_ids = []

    for p in productos:
        title = p.title or ""
        categories = ", ".join([c.name for c in p.categories.all()])
        combined_text = f"{title} {categories}"
        texts.append(combined_text)
        product_ids.append(p.id)

    # 3) Vectorizar con TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    # 4) Ubicar índice del producto actual
    try:
        index = product_ids.index(product_id)
    except ValueError:
        return []

    # 5) Calcular similitud con todos
    sim_scores = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()

    # 6) Quitar el propio producto
    sim_scores[index] = -1

    # 7) Obtener top_n
    top_indices = sim_scores.argsort()[::-1][:top_n]
    top_similar_ids = [product_ids[i] for i in top_indices]

    return top_similar_ids
