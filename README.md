# 🎭 Theatre Booking API

The **Theatre Booking API** is a Django-based web API for managing theatrical events, including plays, performances, actors, halls, and reservations. It uses the Django REST Framework and supports media uploads and user authentication.

## 🔑 Features

### 🎤 Genres

* Create, update, and list genres (e.g., Drama, Comedy, Tragedy).

### 👨‍🎓 Actors

* Manage actor profiles.
* View all actors and their related plays.

### 🌟 Plays

* Create, update, and retrieve play details.
* Each play includes:

  * Title
  * Description
  * Image
  * Genres
  * Actors

### 🎭 Theatre Halls

* Define hall name, seat configuration.
* Upload hall images.

### ⏰ Performances

* Schedule plays with show times and hall assignment.
* Automatically calculate:

  * Total seats
  * Sold tickets
  * Available seats
  * Play genres

### 🎟️ Tickets

* Book seats for specific performances.
* Validate seat placement.

### 📅 Reservations

* Authenticated users can:

  * Reserve tickets for performances.
  * View their reservation history.

### 🔐 Permissions

* **Admins**: Can perform all actions across all endpoints.
* **Authenticated Users**: Can view all public data and create/view their own reservations.
* **Unauthenticated Users**: Can only perform safe methods (GET, HEAD, OPTIONS).

## 📂 API Endpoints

| Resource      | Endpoint              | Permissions                  |
| ------------- | --------------------- | ---------------------------- |
| Plays         | `/api/plays/`         | Admin: Full, Auth: Read-only |
| Actors        | `/api/actors/`        | Admin: Full, Auth: Read-only |
| Genres        | `/api/genres/`        | Admin: Full, Auth: Read-only |
| Theatre Halls | `/api/theatre-halls/` | Admin: Full, Auth: Read-only |
| Performances  | `/api/performances/`  | Admin: Full, Auth: Read      |
| Reservations  | `/api/reservations/`  | Authenticated users only     |
| Tickets       | `/api/tickets/`       | Admin: Full, Auth: Read-only |

## 📁 Media

* Media files (images) for plays and halls are stored in `/media/`.
* Uploads handled via custom image endpoints.

## ✅ Tech Stack

* Python 3.11
* Django 5.2
* Django REST Framework
* PostgreSQL
* JWT Authentication

---

*Designed for managing a theatre booking system with full CRUD capabilities and access control.*


# Theatre API

Theatre API is a Django REST Framework project designed for managing theatrical plays, actors, genres, theatre halls, performances, tickets, and reservations.

## Key Features

* **Genres**: Create and list genres.
* **Actors**: Create, view, and list actors.
* **Theatre Halls**: Create, update, and list halls with images and seating.
* **Plays**: Create, update, retrieve and list plays with associated actors and genres.
* **Performances**: Create, update, and view performances of plays in halls.
* **Tickets**: Automatically created for each seat per performance. View ticket availability and details.
* **Reservations**: Authenticated users can reserve tickets.

### Permissions

* **Admins**: Full access to all endpoints.
* **Authenticated Users**: Can view and reserve tickets, and see performance details.
* **Unauthenticated Users**: Read-only access (GET, HEAD, OPTIONS).

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AndreyHMkr/theatre-tickets.git
cd your-repository-name
```

### 2. Install Dependencies

Make sure you have Python and pip installed:

```bash
pip install -r requirements.txt
```

### 3. Set Up Database

This project uses PostgreSQL. Ensure you have a PostgreSQL instance and set the following environment variables:

```
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Project

```bash
python manage.py runserver
```

Access the API at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Using the API

### 1. Authentication

Uses JWT. Obtain tokens via `/api/user/token/` and `/api/user/token/refresh/`.

### 2. Example Requests

```http
GET /api/genres/
GET /api/actors/
GET /api/plays/
GET /api/performances/
```

### 3. Reservations

To reserve tickets:

```http
POST /api/reservations/
```

Body example:

```json
{
  "tickets": [
    {"row": 1, "seat": 1, "performance": 3},
    {"row": 1, "seat": 2, "performance": 3}
  ]
}
```

### 4. Images

You can upload images for `Play` and `TheatreHall` via:

```http
POST /api/plays/<id>/upload-image/
POST /api/theatre-halls/<id>/upload-image/
```

---

## Docker Usage (Optional)

### Build the Image

```bash
docker build -t theatre-api .
```

### Run with Compose

```bash
docker-compose up
```

Access the app at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Documentation

Generated with `drf-spectacular`. Access Swagger and Redoc:

* Swagger: [http://127.0.0.1:8000/api/doc/swagger/](http://127.0.0.1:8000/api/doc/swagger/)
* Redoc: [http://127.0.0.1:8000/api/doc/redoc/](http://127.0.0.1:8000/api/doc/redoc/)

---

## Project Structure

```
/catalog
    models.py          # Data models
    serializers.py     # DRF serializers
    views.py           # Viewsets
    urls.py            # Route definitions
    permissions.py     # Custom permissions
    utils/             # Upload paths & image handlers
    migrations/
/uploads              # Media storage
/user                 # User app with JWT
```

---

## Database Schema

* **Genre**: Genres of plays.
* **Actor**: Actor names.
* **Play**: Includes actors, genres, and image.
* **TheatreHall**: Rows, seats per row, and image.
* **Performance**: Show time + link to play and hall.
* **Ticket**: One ticket = one seat in a performance.
* **Reservation**: Links user with multiple tickets.

---

## Contact

Created by \[Andrii]. For inquiries, contact \[[grushevoyandrey@gmail.com](..)].
