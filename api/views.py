from .serializers import UserSerializer, RestaurantSerializer, ReviewSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Restaurant, Review
from rest_framework import filters
from .filters import RestaurantFilter, ReviewFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_class = RestaurantFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.max_page_size = 100

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
            # self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    
