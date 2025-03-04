# 🍽️ Restaurant Review Backend API

This is a Django REST framework-based API for managing restaurants and user reviews. The app supports user authentication, role-based access, and geolocation data.

# Installation

## Install Dependencies
```
pip install -r requirements.txt
```
## Set Up Environment Variables
- Remove .example from .env.example in /restaurant_review/.env.example
- Fill all the field
```
DB_ENGINE = ""
DB_NAME = ""
DB_USER = ""
DB_PASSWORD =  ""
DB_HOST = ""
DB_PORT = ""
```
## Apply Migrations & Create Superuser
```
python manage.py migrate
python manage.py createsuperuser
```
## Run the Development Server
```
python manage.py runserver

```

--------------------

## 🔗 **API Endpoints**

### 🏢 **Restaurant Endpoints**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/restaurants/` | List all restaurants |
| GET | `/api/restaurants/{restuarant_id}/` | Get a single restaurant |
| POST | `/api/restaurants/` | Create a restaurant (admin) |
| PATCH | `/api/restaurants/{restuarant_id}/` | Partial update a restaurant (admin) |
| PUT | `/api/restaurants/{restuarant_id}/` | Update a restaurant (admin) |
| DELETE | `/api/restaurants/{restuarant_id}/` | Delete a restaurant (admin) |

### ⭐ **Review Endpoints**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/reviews/` | List all reviews |
| GET | `/api/reviews/{reveiw_id}` | Get a single review |
| POST | `/api/reviews/` | Submit a review (authenticated) |
| PATCH | `/api/reviews/{reveiw_id}/` | Partial update own review (authenticated owner) |
| DELETE | `/api/reviews/{reveiw_id}/` | Delete own review or admin (authenticated owner or admin) |

--------------------
## Filtering, Sorting, and Pagination in the API

### Filtering

This API supports filtering using `django-filter`. The available filters for each endpoint are:

#### Restaurant Filters
You can filter restaurants by:
- `name` (case-insensitive partial match or exact match)

Example usage:
```
GET /api/restaurants/?name__icontains=mcdonalds
GET /api/restaurants/?name__iexact=McDonald's
```

#### Review Filters
You can filter reviews by:
- `rating` (greater than or equal to, less than or equal to)
- `restaurant` (exact match)
- `created_at` (greater than or equal to, less than or equal to)
- `user` (exact match)

Example usage:
```
GET /api/reviews/?rating__gte=4
GET /api/reviews/?rating__lte=3
GET /api/reviews/?restaurant=5
GET /api/reviews/?created_at__gte=2024-01-01
GET /api/reviews/?user=10
```

### Sorting

You can sort results using the `ordering` query parameter.

#### Sorting Restaurants
You can sort restaurants by `name` (ascending or descending):
```
GET /api/restaurants/?ordering=name   # Ascending order (A-Z)
GET /api/restaurants/?ordering=-name  # Descending order (Z-A)
```

#### Sorting Reviews
You can sort reviews by `rating` or `created_at`:
```
GET /api/reviews/?ordering=rating        # Sort by rating (low to high)
GET /api/reviews/?ordering=-rating       # Sort by rating (high to low)
GET /api/reviews/?ordering=created_at    # Sort by oldest first
GET /api/reviews/?ordering=-created_at   # Sort by newest first
```

### Pagination

Pagination is enabled using Django REST Framework’s `LimitOffsetPagination`. The default settings are:
- `default_limit = 25` (25 results per page)
- `max_limit = 100` (Maximum 100 results per page)

To use pagination, use the `limit` to set number of result to show and `offset` to navigate thorugh pages, example:
```
GET /api/restaurants/?limit=25&offset=100
GET /api/reviews/?limit=25&offset=125
```

--------------------

## 🛠 Tech Stack
- Python 3.12.x 🐍
- Django REST Framework 🛠
- PostgreSQL (or SQLite for local development) 🗄️
- Simple JWT 🔑 (for authentication)

