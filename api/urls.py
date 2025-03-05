from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from . import views

router = DefaultRouter()
router.register('restaurants', views.RestaurantViewSet)
router.register('reviews', views.ReviewViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]