from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('restaurant', views.RestaurantViewSet)
router.register('review', views.ReviewViewSet)

urlpatterns = []

urlpatterns += router.urls