import django_filters
from .models import User, Restaurant, Review
 
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