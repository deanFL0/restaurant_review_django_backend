import django_filters
from .models import User, Restaurant, Review

# class TotalRatingFilter(django_filters.FilterSet):
#     total_rating = django_filters.NumberFilter(
#         field_name='total_rating',
#         method='filter_total_rating',
#         label='Total Rating',
#         help_text='Filter by total rating of the restaurant.',
#     )
#     def filter_total_rating(self, queryset, name, value):
#         return queryset.filter(total_rating__gte=value)
    
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
        }