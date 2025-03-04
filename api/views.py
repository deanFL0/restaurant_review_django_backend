from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

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
    pagination_class = PageNumberPagination
    pagination_class.page_size = 25
    pagination_class.max_page_size = 100

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to include all reviews associated with the restaurant.
        """
        instance = self.get_object()
        reviews = Review.objects.filter(restaurant=instance)

        serializer = self.get_serializer(instance)
        data = serializer.data

        data['reviews'] = ReviewSerializer(reviews, many=True).data

        return Response(data, status=status.HTTP_200_OK)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated , IsOwnerOrAdmin]

    # Filter
    filterset_class = ReviewFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'created_at']

    #Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 25
    pagination_class.max_page_size = 100

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        """
        Override create method to automatically set the user and ensure restaurant exists.
        """
        
        restaurant_id = request.data.get("restaurant")

        # Ensure restaurant exists
        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already reviewed this restaurant
        if Review.objects.filter(user=request.user, restaurant=restaurant).exists():
            return Response({"error": "You have already reviewed this restaurant."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the review
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)