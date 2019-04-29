from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:id>', views.individual_view, name="property"),
    path('map/', views.map_view, name="map"),
    path('neighborhoods/', views.neighborhood_list_view, name="neighborhoods"),
    path('neighborhood/<int:id>', views.neighborhood_view, name="neighborhood"),
    path("neighborhoodsearch/", views.neighborhood_search_page, name="neighborhoodsearch"),
    path("doneighborhoodsearch/", views.do_neighborhood_search, name="doneighborhoodsearch")
]
