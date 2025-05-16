from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Category, Product
from django.views.generic import DetailView

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("categories")

        # Búsqueda por título
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        # Filtrado por categoría
        category = self.request.GET.get("category", "")
        if category:
            queryset = queryset.filter(categories__name=category)
        
        # Filtrado por rango de precios
        price_min = self.request.GET.get("price_min", "")
        price_max = self.request.GET.get("price_max", "")
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        # Filtrado por calificación mínima
        rating_min = self.request.GET.get("rating_min", "")
        if rating_min:
            queryset = queryset.filter(average_rating__gte=rating_min)

        # Ordenar resultados
        sort_by = self.request.GET.get("sort_by", "")
        if sort_by == "price_asc":
            queryset = queryset.order_by("price")
        elif sort_by == "price_desc":
            queryset = queryset.order_by("-price")
        elif sort_by == "rating_desc":
            queryset = queryset.order_by("-average_rating")
        else:
            # Por defecto, ordenamos por título (o lo que necesites)
            queryset = queryset.order_by("title")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Enviar todas las categorías para el filtro en el template
        context["categories"] = Category.objects.all().order_by("name")
        
        # Mantener los valores actuales de los filtros
        context["current_search"] = self.request.GET.get("search", "")
        context["current_category"] = self.request.GET.get("category", "")
        context["current_price_min"] = self.request.GET.get("price_min", "")
        context["current_price_max"] = self.request.GET.get("price_max", "")
        context["current_rating_min"] = self.request.GET.get("rating_min", "")
        context["current_sort_by"] = self.request.GET.get("sort_by", "")

        # Obtener paginación
        paginator = context["paginator"]
        page_obj = context["page_obj"]

        # Convertir el rango elidido en una lista explícita para evitar el error de '...'
        elided_range = list(paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1))

        # Filtrar los valores para que solo incluya números enteros o elipsis correctos
        context["elided_page_range"] = [num if isinstance(num, int) else '…' for num in elided_range]

        return context
    
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'asin'
    slug_url_kwarg = 'asin'

