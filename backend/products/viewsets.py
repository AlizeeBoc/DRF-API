from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer

# ho whaou!!!
# Similaire au processus des class ProductMixinView
class ProductViewSet(viewsets.ModelViewSet):
    '''
    http -> function
    get -> list - Queryset
    get -> retrieve -> Product Instance Detail view
    post -> create -> new Instance
    put -> update
    patch -> partial update
    delete -> destroy
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default


class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    '''
    get -> list - Queryset
    get -> retrieve -> Product Instance Detail view
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default

#product_list_view = ProductGenericViewSet.as_view({'get' : 'list'})
#product_detail_view = ProductGenericViewSet.as_view({'get' : 'retrieve'})
