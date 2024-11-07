from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from sistema_fcc_api.serializers import *
from sistema_fcc_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
import string
import random
import json

class ProductosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        productos = Productos.objects.order_by("id")
        productos = ProductosSerializer(productos, many=True).data
        
        #for producto in productos:
        #    producto["entregas"] = json.loads(producto["entregas"])
        
        return Response(productos, 200)
    

class ProductosView(generics.CreateAPIView):
    
    def get(self, request, *args, **kwargs):
        producto = get_object_or_404(Productos, id = request.GET.get("id"))
        producto_data = ProductosSerializer(producto, many=False).data
       # producto["entregas"] = json.loads(producto["entregas"])

        if producto.foto: 
            producto_data["foto"] = request.build_absolute_url(producto.foto.url)
        else:
            producto_data["foto"] = request.build_absolute_uri(settings.DEFAULT_PRODUCTO_URL)  # URL completa de la imagen predeterminada
            
        return JsonResponse(producto_data)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        producto = ProductosSerializer(data=request.data)
        if producto.is_valid():
            
            product_id = request.data.get("id")
            
            
            existing_id = Productos.objects.filter(id=product_id).first()
            
            if existing_id:
                return Response({"message": "id" +id+", is already taken"},400)
            
            producto = Productos.objects.create(
                                                #id = request.data.get("id"),
                                                nombre=request.data.get("nombre"),  # Usando .get() para evitar errores
                                                foto=request.data.get("foto"),
                                                descripcion=request.data.get("descripcion"),
                                                precio=request.data.get("precio"),
                                                unidades=request.data.get("unidades", 0),  # Asignando un valor por defecto en caso de que no exista la clave
                                                entregas=json.dumps(request.data.get("entregas", []))  # Similar con entregas, asegurando que siempre haya un valor (vacío por defecto)
)
            producto.save()
            return Response({"producto_created_id: ": producto.id}, 201)
        return Response(producto.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductosViewEdit(generics.CreateAPIView):
    permissions_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        producto = get_object_or_404(Productos, id=request.data["id"])
        producto.nombre = request.data["nombre"]
        producto.foto = request.data["foto"]
        producto.descripcion = request.data["descripcion"]
        producto.precio = request.data["precio"]
        producto.unidades = request.data["unidades"]
        producto.entregas = json.dumps(request.data["entregas"])
        producto.save()
        
        productos = ProductosSerializer(producto, many=False).data
        
        return Response(productos, 200)
    
    def delete(self, request, *args, **kwargs):
        producto = get_object_or_404(Productos, id=request.GET.get("id"))
        try:
            producto.delete()
            return Response({"details": "Producto Eliminado"}, 200)
        except Exception as e:
            return Response({"details": "No se pudo eliminar"}, 400)
        
        