from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

restaurant_route = DefaultRouter()
restaurant_route.register('restaurant', views.RestaurantViewSet)

urlpatterns = []

urlpatterns += restaurant_route.urls
