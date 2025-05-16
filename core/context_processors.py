def navbar_items(request):
    """
    Retorna un contexto con los ítems de menú a mostrar en la barra de navegación.
    """
    menu_items = []

    if request.user.is_authenticated:
        menu_items = [
            {
                'url_name': 'home',
                'text': 'Inicio',
                'icon_class': 'fas fa-home'
            },
            {
                'url_name': 'perfil',
                'text': 'Perfil',
                'icon_class': 'fas fa-user'
            },
            {
                'url_name': 'product-list',
                'text': 'Catálogo de productos',
                'icon_class': 'fas fa-box-open'
            },
            {
                'url_name': 'recommendation_dashboard',
                'text': 'Recomendaciones',
                'icon_class': 'fas fa-chart-bar'
            },
        ]

        if request.user.is_staff:
            pass  # Aquí podrías agregar más opciones para administradores

    return {'menu_items': menu_items}
