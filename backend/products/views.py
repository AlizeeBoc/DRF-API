from rest_framework import (
    generics,
    mixins,
)  # classes de views génériques simplifiat les CRUD op
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin
from .models import Product
from .serializers import ProductSerializer

# generics views : classe based views [...]


class ProductListCreateAPIView(
    StaffEditorPermissionMixin, 
    generics.ListCreateAPIView):  # classe de vue générique (crée un objet si POST ou les liste si GET)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # indique quel sérializer utiliser pour convertir les Product en JSON
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # cf custom permissions

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")

        if content is None:
            content = title
        serializer.save(content=content)


product_list_create_view = (
    ProductListCreateAPIView.as_view()
)  # as_view() = convertit les classe de vue géné en *fonctions* de vue associables à des urls


class ProductDetailAPIView(
    StaffEditorPermissionMixin, 
    generics.RetrieveAPIView):  # récupère un objet par son id
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # cf custom permissions


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    StaffEditorPermissionMixin, generics.UpdateAPIView
):  # update un objet par son id
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # cf custom permissions

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    StaffEditorPermissionMixin, generics.DestroyAPIView
):  # delete un objet par son id
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # cf custom permissions

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


product_destroy_view = ProductDestroyAPIView.as_view()


# class ProductListAPIView(generics.ListAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer

# product_list_view = ProductListAPIView.as_view()

# on préfèrera transformer la route CreateAPIview en ListCreateAPIview


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"  # pour le retrieveModelMixins

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        #email = serializer.validated_data.pop('email')
        #print(email)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if content is None:
            content = title
        serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()


# [...] Or function based view => may be confusing, best to work with generics.views
@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # produira un message d'erreur
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content")

            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)
