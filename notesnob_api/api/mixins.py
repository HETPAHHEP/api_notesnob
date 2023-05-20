from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin):
    """View set для функций list, create, delete"""
