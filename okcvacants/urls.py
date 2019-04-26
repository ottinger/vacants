from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:id>', views.individual_view, name="property"),
    path('map/', views.map_view, name="map"),
    path('serialized/', views.serialized, name="serialized")
]
