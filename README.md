# Social Networking Application API

This is a Django REST Framework-based API for a social networking application, which includes functionalities for user login/signup, searching users, sending/accepting/rejecting friend requests, and listing friends and pending friend requests.

## Features

- **User Authentication:**
  - Login with email and password (email is case insensitive).
  - Signup with email only (no OTP verification required, but must be a valid email format).
  - All APIs except signup and login require authenticated users.

- **Friend Requests:**
  - Send friend requests.
  - Accept or reject friend requests.
  - List friends.
  - List pending friend requests.

## Endpoints

### User Authentication

- **Signup:**
  - `POST /signup/`
  - Request Body: `{ "username": "user", "email": "user@example.com", "password": "password", "first_name":"first_name", "last_name":"last_name" }`
  
- **Login:**
  - `POST /login/`
  - Request Body: `{ "username": "user", "email": "user@example.com", "password": "password" }`
  - Response: `{ "token": "your-token" }`

### User Search

- **Search Users:**
  - `GET /search/?q=keyword`
  - Pagination: 10 records per page

### Friend Requests

- **Send Friend Request:**
  - `POST /friend-request/`
  - Request Body: `{ "to_user": "recipient_username_or_id" }`
  - Response: `{ "detail": "Friend request sent." }`

- **Accept/Reject Friend Request:**
  - `PATCH /friend-request/<id>/`
  - Request Body: `{ "status": "accepted" }` or `{ "status": "rejected" }`

- **List Friends:**
  - `GET /friends/`
  - Pagination: 10 records per page

- **List Pending Requests:**
  - `GET /pending-requests/`
  - Pagination: 10 records per page

## Setup and Installation

### Requirements

- Python 3.9.13
- Django 4.2.13
- Django REST Framework

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/pc-crazy/django-social-network-api.git
    cd django-social-network-api
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```
