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
| GET | `/api/restaurants/{id}/` | Get a single restaurant |
| POST | `/api/restaurants/` | Create a restaurant (admin) |
| PUT | `/api/restaurants/{id}/` | Update a restaurant (admin) |
| DELETE | `/api/restaurants/{id}/` | Delete a restaurant (admin) |

### ⭐ **Review Endpoints**

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/restaurants/{id}/reviews/` | List reviews for a restaurant |
| POST | `/api/reviews/` | Submit a review (authenticated) |
| PUT | `/api/reviews/{id}/` | Edit own review (authenticated owner) |
| DELETE | `/api/reviews/{id}/` | Delete own review or admin (authenticated owner or admin) |

--------------------

## 🛠 Tech Stack
- Python 3.12.x 🐍
- Django REST Framework 🛠
- PostgreSQL (or SQLite for local development) 🗄️
- Simple JWT 🔑 (for authentication)

