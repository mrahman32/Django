from importlib.resources import path
from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
]
