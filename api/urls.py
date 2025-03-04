from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from . import views

router = DefaultRouter()
router.register('restaurants', views.RestaurantViewSet)
router.register('reviews', views.ReviewViewSet)

nested_router = NestedSimpleRouter(router, r'restaurants', lookup='restaurant')
nested_router.register(r'reviews', views.RestaurantReviewViewSet, basename='restaurant-reviews')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(nested_router.urls)), 
]