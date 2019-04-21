from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:id>', views.individual_view, name="property"),
]
