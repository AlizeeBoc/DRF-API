from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from .models import Product
from .validators import validate_title

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
    view_name="product-detail", 
    lookup_field="pk",
    read_only=True
    )
    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    related_products= ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    my_user_data = serializers.SerializerMethodField(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    # ne fonctionne que sur ModelSerializer :
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk"
    )
    title = serializers.CharField(validators=[validate_title])

    class Meta:
        model = Product
        fields = [
            "owner",  # user_id, a commenter en prod;)
          #  "email",
            "url",
            "edit_url",
            "pk",
            "title",
            "content",
            "price",
            "sale_price",
            "my_discount",
            "my_user_data",
            'related_products',
        ]

    # def validate_title(self, value):
    #    # request = self.context.get('request')
    #    # user = request.user
    #     qs = Product.objects.filter(title__iexact=value) #i pour case insensitive
    #     if qs.exists():
    #          raise serializers.ValidationError(f"{value} is already a product name.")
    #     return value

    # def create(self, validated_data):
    #    email = validated_data.pop('email')
    #    obj = super().create(validated_data)
    #    print(email, obj)
    #    return obj

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_my_user_data(self, obj):
        return {"username": obj.user.username}

    def get_edit_url(self, obj):
        # return f"/api/v2/products/{obj.pk}/"
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    # Si create product, les url seront automatiquement générées

    def get_my_discount(self, obj):
        if not hasattr(obj, "id"):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
