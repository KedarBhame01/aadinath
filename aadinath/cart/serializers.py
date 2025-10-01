from rest_framework import serializers
from .models import Cart

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    

    