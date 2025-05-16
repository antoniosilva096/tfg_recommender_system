from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recommendations.algorithms.content import content_based_recommendations
from recommendations.algorithms.hybrid import hybrid_recommendations
from recommendations.algorithms.knn import knn_recommendations
from .algorithms.collaborative import item_based_collaborative, recommend_similar_products
from products.models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib import messages



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

def recommendation_dashboard(request):
    """
    Vista tradicional con Django templates.
    Permite seleccionar un usuario y un algoritmo
    mediante un formulario POST, luego muestra en
    la misma página los resultados (recomendaciones).
    """
    users = User.objects.all()
    recommendations = []
    selected_user = None
    selected_algo = None

    if request.method == "POST":
        # Recuperar user_id y el algoritmo elegido desde el formulario
        user_id = request.POST.get("user_id")
        algo = request.POST.get("algorithm")

        selected_user = User.objects.filter(pk=user_id).first()
        selected_algo = algo

        if selected_user and selected_algo:
            if selected_algo == "collaborative":
                recommendations = item_based_collaborative(selected_user.id)
            # Descomenta esto si tienes otro algoritmo:
            # elif selected_algo == "matrix":
            #     recommendations = matrix_factor_recommendations(selected_user.id)
            # elif selected_algo == "hybrid":
            #     recommendations = hybrid_recommendations(selected_user.id)
            # ...

    # Renderizar la plantilla con contexto
    return render(
        request,
        "recommendations/dashboard.html",
        {
            "users": users,
            "recommendations": recommendations,
            "selected_user": selected_user,
            "selected_algo": selected_algo,
        },
    )
    
    
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from products.models import Product
from recommendations.models import Review
from recommendations.algorithms.collaborative import recommend_similar_products
from recommendations.algorithms.content import content_based_recommendations
from recommendations.algorithms.knn import knn_recommendations
from recommendations.algorithms.hybrid import hybrid_recommendations

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
