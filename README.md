# 📝 Notes Management REST API

A backend RESTful API built using Django and Django REST Framework to perform CRUD operations on Notes.

## 🚀 Features

- Create a new note
- View all notes
- View a single note
- Update note details
- Delete a note
- JSON based API responses
- Clean project structure following REST principles

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Git & GitHub

## 📂 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | /notes/ | Get all notes |
| GET | /notes/<id>/ | Get single note |
| POST | /notes/ | Create note |
| PUT | /notes/<id>/ | Update note |
| DELETE | /notes/<id>/ | Delete note |

## ▶️ How to Run Project

```bash
git clone https://github.com/Nishu5464/notes-management-api.git
cd notes-management-api
pip install -r requirements.txt
python manage.py runserver
