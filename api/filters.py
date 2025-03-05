import django_filters
from .models import User, Restaurant, Review
 
class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains', 'iexact'],
            'email': ['icontains', 'iexact'],
            'created_at': ['gte', 'lte'],
            'is_active': ['exact'],
            'is_staff': ['exact'],
        }

class RestaurantFilter(django_filters.FilterSet):
    class Meta:
        model = Restaurant
        fields = {
            'name': ['icontains', 'iexact'],
        }

class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = {
            'rating': ['gte', 'lte'],
            'restaurant': ['exact'],
            'created_at': ['gte', 'lte'],
            'user': ['exact'],
        }