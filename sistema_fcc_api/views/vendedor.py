
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

class VendedoresAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        vendedores = Vendedores.objects.filter(user__is_active = 1).order_by("id")
        vendedores = VendedoresSerializer(vendedores, many=True).data
        
        #if not vendedores: 
        #    return Response({},400)
        #for vendedor in vendedores:
        #    vendedor["foto"] = json.loads(vendedor["foto"])
        
        return Response(vendedores, 200)
    
class VendedoresView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        vendedor = get_object_or_404(Vendedores, id = request.GET.get("id"))
        vendedor_data = VendedoresSerializer(vendedor, many=False).data
        
        if vendedor.foto:
            vendedor_data["foto"] = request.build_absolute_uri(vendedor.foto.url)  # URL completa de la imagen
        else:
            vendedor_data["foto"] = request.build_absolute_uri(settings.DEFAULT_FOTO_URL)  # URL completa de la imagen predeterminada
    
        return JsonResponse(vendedor_data)
    

    
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            #Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)


            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            #Create a profile for the user
            vendedor = Vendedores.objects.create(user=user,
                                            #id= request.data["id"],
                                            telefono= request.data["telefono"],
                                            edad = request.data["edad"],
                                            foto = request.data["foto"])
                                            
            vendedor.save()

            return Response({"vendedor_created_id": vendedor.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendedoresViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        # iduser=request.data["id"]
        vendedor = get_object_or_404(Vendedores, id=request.data["id"])
        vendedor.id = request.data["id"]
        vendedor.telefono = request.data["telefono"]
        vendedor.edad = request.data["edad"]
        vendedor.foto = request.data["foto"]
        vendedor.save()
        temp = vendedor.user
        temp.first_name = request.data["first_name"]
        temp.last_name = request.data["last_name"]
        temp.save()
        user = VendedoresSerializer(vendedor, many=False).data

        return Response(user,200)
    
    #Eliminar vendedor 
    def delete(self, request, *args, **kwargs):
        vendedor = get_object_or_404(Vendedores, id=request.GET.get("id"))
        try:
            vendedor.user.delete()
            return Response({"details":"Vendedor eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)