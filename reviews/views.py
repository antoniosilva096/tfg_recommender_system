
from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Vista para listar, crear, actualizar y eliminar reseñas.
    """
    queryset = Review.objects.all().select_related('user', 'product')
    serializer_class = ReviewSerializer
