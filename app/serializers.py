# myapp/serializers.py
from django.contrib.auth.forms import AuthenticationForm  
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password1', 'password2']

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match.')

        return data

    def create(self, validated_data):
       
        validated_data.pop('password1', None)
        validated_data.pop('password2', None)

        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        form = AuthenticationForm(data=self.initial_data)
        if form.is_valid():
            data['user'] = form.get_user()
        else:
            raise serializers.ValidationError('Unable to log in with provided credentials.')
        return data
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'stock', 'description']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'order_status']
