from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, NotFound, ValidationError

from .filters import RestaurantFilter, ReviewFilter, UserFilter
from .models import Restaurant, Review, User
from .permissions import IsOwnerOrAdmin
from .serializers import RestaurantSerializer, ReviewSerializer, UserSerializer, RegisterSerializer, ChangePasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    # Filter
    filterset_class = UserFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['username', 'email', 'created_at']

    # Pagination
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 25
    pagination_class.max_limit = 100

    def get_permissions(self):
        """Set permissions dynamically based on action"""
        if self.action in ['create', 'register']:
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'list':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST", "Use the /api/users/register/ endpoint to create users.")
    
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        """Public registration endpoint"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsOwnerOrAdmin])
    def change_password(self, request, username=None):
        """Change user password"""
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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