from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.ViewSetMixin):
    """View set для функций list, create, delete"""
