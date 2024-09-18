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

class ClienteAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        cliente = Clientes.objects.filter(user__is_active = 1).order_by("id")
        lista = ClientesSerializer(cliente, many=True).data
        
        return Response(lista, 200)
    
class ClienteView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        cliente = get_object_or_404(Clientes, id = request.GET.get("id"))
        cliente = ClientesSerializer(cliente, many=False).data

        return Response(cliente, 200)
    
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
            cliente = Clientes.objects.create(user=user,
                                            edad= request.data["edad"],
                                            foto = request.data["foto"])
            cliente.save()

            return Response({"cliente_created_id": cliente.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClienteViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        # iduser=request.data["id"]
        cliente = get_object_or_404(Clientes, id=request.data["id"])

        cliente.edad = request.data["edad"]
       
        cliente.save()
        temp = cliente.user
        temp.first_name = request.data["first_name"]
        temp.last_name = request.data["last_name"]
        temp.foto = request.data["foto"]
        temp.save()
        user = ClientesSerializer(cliente, many=False).data

        return Response(user,200)
    
    #Eliminar alumno
    def delete(self, request, *args, **kwargs):
        cliente = get_object_or_404(Clientes, id=request.GET.get("id"))
        try:
            cliente.user.delete()
            return Response({"details":"Cliente eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)