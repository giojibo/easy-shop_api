from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from easy_shop_Api.serializers import *
from easy_shop_Api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets

class ComentariosView(generics.ListCreateAPIView):
    "Vista para listar y crear comentarios asociados a un producto."
    serializer_class = ComentariosSerializer

    def get_queryset(self):
        "Filtra los comentarios por producto."
        producto_id = self.request.GET.get("producto_id")
        return Comentarios.objects.filter(producto_id=producto_id)

    def post(self, request, *args, **kwargs):
        "Crea un nuevo comentario para un producto."
        comentario_serializer = ComentariosSerializer(data=request.data)
        if comentario_serializer.is_valid():
            # Aquí puedes asignar el usuario autenticado al comentario si es necesario
            comentario_serializer.save()
            return Response(comentario_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comentario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComentariosEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    "Vista para editar o eliminar un comentario."
    queryset = Comentarios.objects.all()
    serializer_class = ComentariosSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        "Actualiza un comentario existente."
        comentario = self.get_object()
        
        # Actualizar los campos del comentario
        comentario.contenido = request.data.get("contenido", comentario.contenido)
        comentario.calificacion = request.data.get("calificacion", comentario.calificacion)
        comentario.save()

        return Response(ComentariosSerializer(comentario).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        "Elimina un comentario por ID."
        comentario = self.get_object()
        comentario.delete()
        return Response({"details": "Comentario eliminado"}, status=status.HTTP_200_OK)
