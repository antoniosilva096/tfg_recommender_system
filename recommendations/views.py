from datetime import timedelta
import math
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from recommendations.algorithms.content import content_based_recommendations
from recommendations.algorithms.hybrid import hybrid_recommendations
from recommendations.algorithms.knn import knn_recommendations
from .algorithms.collaborative import item_based_collaborative, recommend_similar_products
from products.models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from products.models import Product
from recommendations.models import RecommendationEvaluation, Review
from recommendations.algorithms.collaborative import recommend_similar_products
from recommendations.algorithms.content import content_based_recommendations
from recommendations.algorithms.knn import knn_recommendations
from recommendations.algorithms.hybrid import hybrid_recommendations



@api_view(["GET"])
def recommend_products(request, user_id):
    """
    Endpoint DRF para obtener recomendaciones vía JSON.
    user_id es el 'pk' del usuario en Django.
    Retorna un JSON con los IDs de productos recomendados.
    """
    recommended_pids = item_based_collaborative(user_id)
    return Response({
        "user_id": user_id,
        "recommended_products": recommended_pids
    })

def evaluation_dashboard(request):
    now = datetime.now()
    algorithms = [
        ('collaborative', 'Filtrado Colaborativo'),
        ('content', 'Content-Based'),
        ('svd', 'SVD Matrix Factorization'),
        ('knn', 'K-Nearest Neighbors'),
        ('hybrid', 'Híbrido'),
    ]
    metrics = [
        ('rmse', 'RMSE'),
        ('mae', 'MAE'),
        ('precision', 'Precision@K'),
        ('recall', 'Recall@K'),
        ('ctr', 'Click Through Rate'),
        ('avg_cart_value', 'Valor Medio Carrito'),
    ]
    avg_values = [
        {'algorithm': 'collaborative', 'avg': 1.08},
        {'algorithm': 'content', 'avg': 0.97},
        {'algorithm': 'svd', 'avg': 0.92},
        {'algorithm': 'knn', 'avg': 0.89},
        {'algorithm': 'hybrid', 'avg': 0.87},
    ]
    # Fake evolución temporal con oscilaciones
    time_series = []
    for i in range(29, -1, -1):
        day = now - timedelta(days=i)
        date_iso = day.strftime('%Y-%m-%dT%H:%M:%S')
        for idx, (algo, _) in enumerate(algorithms):
            # Un valor oscilante y distinto para cada algoritmo y cada día
            value = round(
                0.8 + 0.05 * idx + 0.12 * math.sin(i / 3.0 + idx) + 0.07 * math.cos(i / 5.0 + idx * 2),
                3
            )
            time_series.append({
                'timestamp': date_iso,
                'algorithm': algo,
                'value': value,
            })

    context = {
        'algorithms': algorithms,
        'metrics': metrics,
        'selected_algorithms': [],
        'selected_metric': '',
        'days_range': 30,
        'avg_values': avg_values,
        'time_series': time_series,
    }
    return render(request, 'recommendations/dashboard.html', context)


    
    


def recommend_product_page(request, asin):
    product = get_object_or_404(Product, asin=asin)
    recommendations = []
    selected_algorithm = None
    k_value = None
    alpha = None

    if request.method == "POST":
        selected_algorithm = request.POST.get("algorithm")

        if selected_algorithm == "collaborative":
            recommendations = recommend_similar_products(product.id)

        elif selected_algorithm == "content":
            recommendations = content_based_recommendations(product.id)

        elif selected_algorithm == "svd":
            if request.user.is_authenticated:
                from recommendations.algorithms.svd import svd_recommendations
                recommendations = svd_recommendations(request.user.id)
            else:
                messages.warning(request, "Debes estar logueado para usar SVD.")

        elif selected_algorithm == "knn":
            try:
                k_value = int(request.POST.get("k_value", 10))
                recommendations, error_msg = knn_recommendations(product.id, k=k_value)
                if error_msg:
                    messages.warning(request, error_msg)
            except ValueError:
                messages.error(request, "K debe ser un número entero.")

        elif selected_algorithm == "hybrid":
            try:
                alpha = float(request.POST.get("alpha", 0.5))
                recommendations = hybrid_recommendations(product.id, alpha=alpha)
            except ValueError:
                messages.error(request, "Alpha debe ser un número decimal entre 0 y 1.")

        # Limitamos a 4 recomendaciones
        recommendations = recommendations[:4]

    recommended_products = Product.objects.filter(id__in=recommendations)

    return render(
        request,
        'recommendations/recommend_product.html',
        {
            'product': product,
            'selected_algorithm': selected_algorithm,
            'recommended_products': recommended_products,
            'k_value': k_value,
            'alpha': alpha,
        }
    )
