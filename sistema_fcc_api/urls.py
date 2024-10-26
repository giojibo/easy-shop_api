"""point_experts_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from sistema_fcc_api.views import bootstrap
from sistema_fcc_api.views import users
from sistema_fcc_api.views import auth
from sistema_fcc_api.views import cliente
from sistema_fcc_api.views import vendedor
from sistema_fcc_api.views import productos

urlpatterns = [
    #Version
        path('bootstrap/version', bootstrap.VersionView.as_view()),
    #Create User
        path('admin/', users.AdminView.as_view()),
        #Admin Data
       # path('lista-admin/', users.AdminAll.as_view()),
        #Editar Admin 
       #  path('admin-edit/', users.AdminViewEdit.as_view()),
        #Create Alumnos
        path('cliente/', cliente.ClienteView.as_view()),
        #Alumnos Data
      ##path('lista-alumno/', cliente.AlumnoAll.as_view()),
        #Editar alumnos
       path('cliente-edit/', cliente.ClienteViewEdit.as_view()),
        #Creater Maestros
        path('vendedor/', vendedor.VendedoresView.as_view()),
        #Maestros Data
       #path('lista-maestro/', vendedor.MaestroAll.as_view()),
        #Editar maestro
       path('vendedor-edit/', vendedor.VendedoresViewEdit.as_view()),
        #registrar Productos
        path('productos/', productos.ProductosView.as_view()),
        #Productos data
        path('lista-productos/', productos.ProductosAll.as_view()),
        #editar productos
       path('productos-edit/', productos.ProductosViewEdit.as_view()),
    #Login
        path('token/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
