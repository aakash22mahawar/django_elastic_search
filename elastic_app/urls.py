from django.contrib import admin
from django.urls import path, include
from elastic_app  import views

urlpatterns = [
    path("search/", views.search_view, name='search'),
]
