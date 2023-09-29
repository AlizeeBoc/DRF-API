from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
    view_name="product-detail", 
    lookup_field="pk",
    read_only=True
    )
    title = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    # ton understand nested datas (but not useful in this case):
#    other_products = serializers.SerializerMethodField(read_only=True)

## Foreign key relationship:
#    def get_other_products(self, obj):
#        #request = self.context.get('request')
#        print(obj) #>> staff
#        user = obj
#        my_products_qs = user.product_set.all()[:5] # 5 related products
#        return UserProductInlineSerializer(my_products_qs, many=True, context= self.context).data