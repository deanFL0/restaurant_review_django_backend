import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.timesince import timesince

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        SUPER_ADMIN = 'super_admin'
    user_id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=Role, default=Role.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    @property
    def total_reviews(self):
        """
        Calculates total reviews made by user.
        Returns:
            int: Total reviews made by user.
        """
        return self.reviews.count()
    
class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='restaurant_images/')
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    @property
    def total_rating(self):
        """
        Calculates the average rating for the restaurant based on all reviews.
        Returns:
            float: The average rating rounded to one decimal place, or 0 if no ratings exist.
        """
        rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(rating,1) if rating else 0
    
    @total_rating.setter
    def set_bar(self, obj):
        if not isinstance(obj, function):
            raise TypeError(
                f"obj must be a function, not {obj.__class__.__name__}"
            )
        self.total_rating = obj
    
    @property
    def total_reviews(self):
        return self.reviews.count()

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    rating = models.IntegerField() #1-5
    review = models.TextField()
    created_at = models.DateField(auto_now_add=timezone.now)
    updated_at = models.DateField(auto_now=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')

    @property
    def user_username(self):
        return self.user.username
    
    @property
    def time_since_posted(self):
        """
        Returns the time elapsed since the review was created.
        Returns:
            str: A human-readable time difference (e.g., "2 days ago").
        """
        return timesince(self.created_at)
    
    @property
    def is_edited(self):
        """
        Checks if the review has been edited.

        Returns:
            bool: True if the review has been updated after creation, False otherwise.
        """
        return self.created_at != self.updated_at