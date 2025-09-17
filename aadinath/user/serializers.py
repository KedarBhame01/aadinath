from rest_framework import serializers
from .models import User

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class User_login_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class User_search_serializer(serializers.Serializer):   
    search_term = serializers.CharField(required=True)
    search_in = serializers.ChoiceField(
        choices=['email']
    )
    