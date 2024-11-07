from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

#from sistema_fcc_api.settings import vendedor_image_upload_to

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    edad = models.IntegerField(null=True, blank=True)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.first_name+" "+self.last_name

class Clientes (models. Model): 
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    edad = models.IntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='images/perfil/cliente', blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "Perfil del cliente: "+self.first_name+" "+self.last_name
    
class Vendedores (models. Model): 
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='images/perfil/vendedores', default='images/perfil/no-image.png')
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "Perfil del vendedor: "+self.first_name+" "+self.last_name
    
    
class Productos (models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='images/productos', default='images/productos/no-product.jpg')
    descripcion = models.TextField(null= True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidades = models.IntegerField(null=True, blank=True)
    entregas = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "Productos" + self.nombre+" Producto: "+ self.id

class Comentarios(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    contenido = models.TextField()
    calificacion = models.IntegerField()  # Campo para la calificación
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario}: {self.contenido}"
    
    
