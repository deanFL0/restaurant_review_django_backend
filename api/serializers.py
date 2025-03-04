from rest_framework import serializers
from .models import User, Restaurant, Review

class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = (
            'uuid',
            'first_name',
            'last_name',
            'username',
            'email',
        )

class RestaurantSerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = (
            'restaurant_id',
            'name',
            'image',
            'description',
            'address',
            'latitude',
            'longitude',
            'website',
            'total_rating',
            'total_reviews',
        )
        read_only_fields = ('total_rating', 'total_reviews')  # Ensure these fields are read-only

    def get_total_rating(self, obj):
        """Retrieve the restaurant's total rating from the model property."""
        return obj.total_rating

    def get_total_reviews(self, obj):
        """Retrieve the count of reviews for the restaurant."""
        return obj.reviews.count()

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField()
    time_since_posted = serializers.ReadOnlyField()
    class Meta:
        model = Review
        fields = (
            'review_id',
            'rating',
            'review',
            'user',
            'restaurant',
            'user_username',
            'time_since_posted',
        )
        read_only_fields = ['user']

    def validate_rating(self, value):
        if value <= 0 or value > 5:
            raise serializers.ValidationError("Rating must be between one to five.")
        return value