from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    #ne fonctionne que sur ModelSerializer :
    url = serializers.HyperlinkedIdentityField(
         view_name='product-detail',
         lookup_field='pk'
    )
    title = serializers.CharField(validators=[validate_title])

    #name = serializers.CharField(source='title', read_only=True)
    #email = serializers.EmailField(write_only=True)
    class Meta:
        model = Product
        fields = [
            'user', # a commenter en prod;)
            'url',
            'edit_url',
            #'email',
            'pk',
            'title',
            #'name', 
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]

    #def validate_title(self, value):
    #    # request = self.context.get('request')
    #    # user = request.user
    #     qs = Product.objects.filter(title__iexact=value) #i pour case insensitive
    #     if qs.exists():
    #          raise serializers.ValidationError(f"{value} is already a product name.")
    #     return value

    #def create(self, validated_data):
    #    email = validated_data.pop('email')
    #    obj = super().create(validated_data)
    #    print(email, obj)
    #    return obj
    
    #def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_edit_url(self, obj):
         #return f"/api/v2/products/{obj.pk}/"
         request = self.context.get('request')
         if request is None:
              return None
         return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)
    #Si create product, les url seront automatiquement générées

    def get_my_discount(self, obj):
            if not hasattr(obj, 'id'):
                 return None
            if not isinstance(obj, Product):
                 return None
            return obj.get_discount()



