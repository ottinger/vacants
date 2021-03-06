from django.urls import path

from . import views

urlpatterns = [
    path('', views.map_view, name='root'),
    path('properties/', views.property_list_view, name='properties'),
    path('property/', views.property_view, name="property"),
    path('property/<int:id>', views.property_view, name="property"),
    path('map/', views.map_view, name="map"),
    path('neighborhoods/', views.neighborhood_list_view, name="neighborhoods"),
    path('neighborhood/', views.neighborhood_view, name="neighborhood"),
    path('neighborhood/<int:id>', views.neighborhood_view, name="neighborhood"),
    path("neighborhoodsearch/", views.neighborhood_search_page, name="neighborhoodsearch"),
    path("doneighborhoodsearch/", views.do_neighborhood_search, name="doneighborhoodsearch"),
    path("propertysearch/", views.property_search_page, name="propertysearch"),
    path("dopropertysearch/", views.do_property_search, name="dopropertysearch"),
    path("export/csv/", views.export_csv, name="exportcsv"),
    path("about/", views.about_page, name="aboutpage")
]
