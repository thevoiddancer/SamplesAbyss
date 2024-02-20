from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='samples-home'),
    path('browse/', views.browse, name='samples-browse'),
    path('search/', views.search, name='samples-search'),
    path('contribute/', views.contribute, name='samples-contribute'),
]
