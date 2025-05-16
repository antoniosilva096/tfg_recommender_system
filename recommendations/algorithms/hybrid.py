from recommendations.algorithms.content import content_based_recommendations
from recommendations.algorithms.collaborative import recommend_similar_products
from products.models import Product

def hybrid_recommendations(product_id, alpha=0.5, top_n=4):
    """
    Recomienda productos combinando filtrado colaborativo y content-based.
    """
    content_ids = content_based_recommendations(product_id, top_n=100)
    collab_ids = recommend_similar_products(product_id, top_n=100)

    content_scores = {pid: 1.0 / (idx + 1) for idx, pid in enumerate(content_ids)}
    collab_scores = {pid: 1.0 / (idx + 1) for idx, pid in enumerate(collab_ids)}

    all_product_ids = set(content_scores.keys()) | set(collab_scores.keys())

    combined_scores = {}
    for pid in all_product_ids:
        score = alpha * collab_scores.get(pid, 0) + (1 - alpha) * content_scores.get(pid, 0)
        combined_scores[pid] = score

    sorted_ids = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    filtered_ids = [pid for pid, score in sorted_ids if pid != product_id]
    
    
    print("📦 Content-based:", content_ids[:5])
    print("🤝 Collaborative:", collab_ids[:5])
    print("🎯 Resultados combinados:", filtered_ids[:4])
    


    return filtered_ids[:top_n]
