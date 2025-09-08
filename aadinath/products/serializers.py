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
        
    def to_representation(self, instance):
          """Add absolute URLs for files in the response."""
          representation = super().to_representation(instance)
          request = self.context.get('request')

          if instance.image and hasattr(instance.image, 'url'):
               representation['image'] = request.build_absolute_uri(instance.image.url)
          else:
               representation['image'] = None

          return representation

