from importlib.resources import path
from xml.etree.ElementInclude import include
from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", view=views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results", view=views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", view=views.vote, name="vote"),
]
