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
        producto = ProductosSerializer(producto, many=False).data
       # producto["entregas"] = json.loads(producto["entregas"])
        
        return Response(producto, 200)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        producto = ProductosSerializer(data=request.data)
        if producto.is_valid():
            id = request.data["id"]
            
            existing_nrc = Productos.objects.filter(id=id).first()
            
            if existing_nrc:
                return Response({"message": "id" +id+", is already taken"},400)
            
            producto = Productos.objects.create( id = request.data["id"], 
                                               nombre = request.data["nombre"],
                                               foto = request.data["foto"],
                                               descripcion = request.data["descripcion"],
                                               precio = request.data["precio"],
                                               unidades = request.data["unidades"],
                                               entregas = json.dumps(request.data["entregas"]),
                                              
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
        
        