# 📝 Production-Grade Notes Management REST API

An upgraded, secure, and highly optimized backend RESTful API built using Django, Django REST Framework (DRF), MySQL, and Redis Caching.

## 🚀 Key Upgrades & Features

1. **User Authentication & Privacy**: 
   - Native DRF Token Authentication.
   - Individual user workspaces: users can only perform CRUD operations on notes **they own**.
2. **Flexible Database Engine**:
   - Out-of-the-box support for MySQL database integration.
   - Fallback toggle to SQLite for seamless offline testing.
3. **Redis Cache-Aside Pattern**:
   - Caching of notes lists per-user to reduce database reads and achieve sub-10ms response times.
   - **Active Cache Invalidation**: Caches are cleared instantly whenever a user creates, updates, or deletes a note.

---

## 🛠 Tech Stack

- **Backend Logic:** Python, Django, Django REST Framework (DRF)
- **Databases:** MySQL (relational database), SQLite (fallback local database)
- **Caching & Key-Value Store:** Redis (`django-redis` backend client)
- **API Client / Testing:** Postman
- **Version Control:** Git & GitHub

---

## 📂 API Reference

All requests require the header `Authorization: Token <your_token>` except for authentication endpoints.

### Authentication Endpoints

| Method | Endpoint | Payload | Description |
|---|---|---|---|
| **POST** | `/api/auth/register/` | `{"username": "...", "password": "...", "email": "..."}` | Create a user account and get a token |
| **POST** | `/api/auth/login/` | `{"username": "...", "password": "..."}` | Log in and obtain your auth token |

### Notes Endpoints

| Method | Endpoint | Query Parameters | Description |
|---|---|---|---|
| **GET** | `/api/notes/` | `?search=query` (Optional) | Get all notes for the authenticated user (Cached) |
| **GET** | `/api/notes/<id>/` | None | Get a specific note |
| **POST** | `/api/notes/` | `{"title": "...", "description": "..."}` | Create a note (Invalidates list cache) |
| **PUT** | `/api/notes/<id>/` | `{"title": "...", "description": "..."}` | Edit a note (Invalidates list cache) |
| **DELETE**| `/api/notes/<id>/` | None | Delete a note (Invalidates list cache) |

---

## ▶️ Setup & Execution Guide

### 1. Install Dependencies
Run the following command to install Django, DRF, Redis support, and database drivers:
```bash
pip install -r requirements.txt
```

### 2. Configure Database & Caching
- **Database (MySQL)**: 
  - In `notesapi/settings.py`, configure the MySQL credentials inside `DATABASES`.
  - Set `USE_MYSQL = True`.
  - *If you don't have MySQL installed locally yet, keep `USE_MYSQL = False` to run on SQLite.*
- **Cache (Redis)**:
  - Make sure your local Redis server is running (default port `6379`).
  - To test caching on Windows, you can start Redis via Docker:
    ```bash
    docker run -d --name local-redis -p 6379:6379 redis
    ```

### 3. Run Database Migrations
Create and execute migrations to update the database schema (this adds the User owner field and timestamp fields):
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Server
```bash
python manage.py runserver
```

---

## 🧪 Postman Verification Guide

To test the security and Redis caching flow:

1. **Register**: Send a `POST` request to `http://127.0.0.1:8000/api/auth/register/` with a JSON body:
   ```json
   {
     "username": "developer_nishant",
     "email": "nishant@example.com",
     "password": "securepassword123"
   }
   ```
   *Copy the `token` key returned in the response.*

2. **Access Security**: Try to call `GET http://127.0.0.1:8000/api/notes/`. You will get a `401 Unauthorized` response.
3. **Authenticate**: In Postman, go to **Headers** and add:
   - Key: `Authorization`
   - Value: `Token <paste_your_copied_token_here>`
4. **Create a Note**: Send a `POST` to `/api/notes/` with a note title and description.
5. **Verify Caching Flow**:
   - Send `GET /api/notes/` (authenticated). Look at the response time in Postman (e.g., 45ms). This was a **Cache Miss**; the system queried the MySQL/SQLite database.
   - Send `GET /api/notes/` again. Look at the response time (e.g., 2ms–5ms). This was a **Cache Hit**; the system retrieved the notes list directly from Redis.
   - Update or delete the note via `PUT` or `DELETE` to `/api/notes/<id>/`.
   - Send `GET /api/notes/` again. The response time will briefly go up (e.g., 40ms) because the previous edit invalidated the Redis cache, forcing the backend to query the database and re-cache the updated data.
