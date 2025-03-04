from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, NotFound, ValidationError

from .filters import RestaurantFilter, ReviewFilter
from .models import Restaurant, Review
from .permissions import IsOwnerOrAdmin
from .serializers import RestaurantSerializer, ReviewSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    # Filter
    filterset_class = RestaurantFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name']

    # Pagination
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 25
    pagination_class.max_limit = 100

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Filter
    filterset_class = ReviewFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'created_at']

    #Pagination
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 25
    pagination_class.max_limit = 100

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()
    
    def put(self, request, *args, **kwargs):
        """
        Don't allow PUT requests.
        """
        raise MethodNotAllowed("PUT")

    def create(self, request, *args, **kwargs):
        """
        Override create method to automatically set the user and ensure restaurant exists.
        """
        
        restaurant_id = request.data.get("restaurant")

        # Ensure restaurant exists
        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise NotFound("Restaurant does not exist.")
        # Check if the user already reviewed this restaurant
        if Review.objects.filter(user=request.user, restaurant=restaurant).exists():
            raise ValidationError("You have already reviewed this restaurant.")

        # Save the review
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)