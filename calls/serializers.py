from rest_framework import serializers
from .models import Product, State


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']  # Add more fields as needed

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = '__all__'