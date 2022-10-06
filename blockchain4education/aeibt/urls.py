from django.urls import path

from . import views

app_name = "aeibt"
urlpatterns = [
    path("btstudents/", views.index),
]
