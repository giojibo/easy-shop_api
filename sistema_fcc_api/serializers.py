from rest_framework import serializers
from rest_framework.authtoken.models import Token
from sistema_fcc_api.models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = "__all__"

class ClientesSerializer(serializers.ModelSerializer): 
    user=UserSerializer(read_only=True)
    foto = serializers.ImageField(use_url=True)  
    class Meta: 
        model = Clientes
        fields = "__all__"
        
class VendedoresSerializer(serializers.ModelSerializer): 
    user=UserSerializer(read_only=True)
    foto = serializers.ImageField(use_url=True)  
    
    class Meta: 
        model = Vendedores
        fields = "__all__"
        
class ProductosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(required=True)
    
    class Meta:
        model = Productos
        fields = ('id', 'nombre')
        
class ProductosSerializer(serializers.ModelSerializer):
    productos = ProductosSerializer(read_only=True)
    
    class Meta:
        model = Productos
        fields = "__all__"
        