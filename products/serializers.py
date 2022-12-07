from rest_framework import serializers
from .models import Product
from users.serializers import UserSerializer

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description','price','quantity','is_active','seller_id','id']


class DetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        depth=1
    
    def create(self,validate_data:dict):
        
        return Product.objects.create(**validate_data)
