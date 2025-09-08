from rest_framework import serializers
from .models import Products

class product_serializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False) 
    category_id = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, default=0)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, required=False, default=0)
    rating = serializers.FloatField(default=0)
    reviews = serializers.IntegerField(default=0)

    class Meta:
        model = Products
        fields = '__all__'
