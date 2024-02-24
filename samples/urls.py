from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='samples-home'),
    path('browse/', views.browse, name='samples-browse'),
    path('search/', views.search, name='samples-search'),
    path('search/song-search', views.song_search_view, name='song-search-results'),
    path('search/sample-search', views.sample_search_view, name='samples-search-results'),
    path('contribute/', views.contribute, name='samples-contribute'),
]
