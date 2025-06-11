# Word Frequency Counter: TF-IDF Analyzer API

A Flask-based backend that exposes endpoints for uploading .txt documents,
organizing them into collections, and computing text statistics like TF-IDF. It
also manages users and system metrics, with a minimal frontend included for
basic interaction.

---

## Contents

* [Project Structure](#-project-structure)
* [Entities Involved](#%EF%B8%8F-entities-involved)
* [How to Run the App](#-how-to-run-the-app)
* [Environment Variables](#%EF%B8%8F-environment-variables)
* [API Documentation](#-api-documentation)
  * [API Endpoints](#%EF%B8%8F-api-endpoints)
  * [Interactive API Docs](#-interactive-api-docs)
* [App Version](#-app-version)
* [Recent Changes](#-recent-changes)
* [References](#-references)

---

## 📁 Project Structure

```
freq_counter/
│
├── app/                          # Main Flask application package
│   │
│   ├── collections/              # Management of document groupings
│   │   ├── __init__.py                
│   │   ├── api_models.py         # API schema definitions
│   │   ├── api_routes.py         # JSON API endpoints 
│   │   ├── decorators.py         # Decorators for validating collections before operating over them
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── namespace.py          # Namespace registration, like a blueprint
│   │   ├── routes.py             # Placeholder for future web views
│   │   └── services.py           # Business logic 
│   │
│   ├── documents/                # Handles document upload, processing, and metadata
│   │   ├── __init__.py
│   │   ├── api_models.py         # API schema definitions 
│   │   ├── api_routes.py         # JSON API endpoints 
│   │   ├── decorators.py         # Decorators for validating documents before operating over them
│   │   ├── error_handlers.py     # Custom error handlers 
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── namespace.py          # Namespace registration, like a blueprint
│   │   ├── routes.py             # Placeholder for future web views
│   │   └── services.py           # Business logic 
│   │
│   ├── media/                    # Directory for storing uploaded text documents
│   │
│   ├── shared/                   # Shared helpers and base components
│   │   ├── __init__.py
│   │   ├── common_models.py      # Reusable SQLAlchemy models
│   │   ├── exceptions.py         # Custom exception classes
│   │   ├── file_utils.py         # Utility functions for validating files
│   │   └── tfidf_stats.py        # Helpers for calculating TF-IDF values
│   │
│   ├── system/                   # Tracks runtime metrics, logs, and app status
│   │   ├── __init__.py
│   │   ├── api_routes.py         # JSON endpoints for system health, metrics, logs
│   │   ├── models.py             # Models for system metrics information 
│   │   ├── namespace.py          # Namespace registration, like a blueprint
│   │   └── services.py           # Aggregates and computes metrics or status values
│   │
│   ├── templates/                # Jinja2 HTML templates (used in `routes.py`)
│   │
│   ├── tfidf/                    # Web interface for documents uploading (not fully implemented)
│   │   ├── __init__.py
│   │   ├── routes.py             # HTML endpoints for viewing TF-IDF results
│   │   └── services.py           # Business logic 
│   │
│   ├── users/                    # Authentication and user management
│   │   ├── __init__.py
│   │   ├── api_models.py         # API schema definitions
│   │   ├── api_routes.py         # JSON endpoints for login, register, etc.
│   │   ├── decorators.py         # Decorators checking authorization
│   │   ├── models.py             # User related models
│   │   ├── namespace.py          # Namespace registration, like a blueprint
│   │   └── services.py           # Password hashing, token logic, etc.
│   │
│   ├── __init__.py               # Flask app factory which creates and configures the app
│   ├── config.py                 # Config classes 
│   ├── database.py               # SQLAlchemy engine initialization
│   └── version.py                # App version info
│
├── migrations/                   # Alembic migrations
├── nginx/                        # Nginx related configurations
├── .dockerignore                 
├── .env                          
├── .env.example                  # Sample .env
├── .gitignore                    
├── CHANGELOG.md                  
├── docker-compose.yml            
├── Dockerfile                     
├── README.md                     
├── requirements.txt              
└── run.py                        
```

---

## 🖼️ Entities Involved

<img width="1018" alt="Screenshot 2025-06-09 at 23 06 36" src="https://github.com/user-attachments/assets/6e8e9039-23c9-4d4c-be04-e14a6ce6442b" />

### 📄 Documents

- `id`: Primary key
- `name`: Original file name
- `contents`: Text content of the file
- `content_hash`: SHA256 hash of contents (to detect duplicates)
- `user_id`: Foreign key to `Users` (owner of the document)
- `created_at`: Timestamp of upload

### 👤 Users

- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password
- `created_at`: Timestamp of registration

### 🔗 Documents_Collections (Association Table)

- `document_id`: Foreign key to `Documents`
- `collection_id`: Foreign key to `Collections`
- `created_at`: Timestamp when the document was added to the collection

### 🗂️ Collections

- `id`: Primary key
- `name`: Name of the collection
- `user_id`: Foreign key to `Users` (owner of the collection)
- `created_at`: Timestamp of creation

### 📊 File_Metrics

- `id`: Primary key
- `filename`: Name of the uploaded file
- `word_count`: Total number of words
- `file_size`: File size in bytes
- `created_at`: Timestamp of metric entry

---

## 🚀 How to Run the App

### 🐳 Using Docker

1. **Clone the repository**

   ```bash
   git clone https://github.com/AmalSultanov/freq_counter
   cd freq_counter
   ```

2. **Create a `.env` file and set environment variables in any editor**

   Refer to the [⚙️ Environment Variables](#-environment-variables) section for clarification.

   ```bash
   cp .env.example .env
   nano .env
   ```

3. **Build and run using Docker Compose**

   ```bash
   docker compose up --build
   ```

4. The app will be available at [`http://127.0.0.1`](http://127.0.0.1). Interactive Swagger docs will be available at [`http://127.0.0.1/api/docs`](http://127.0.0.1/api/docs)

---

## ⚙️ Environment Variables

The application uses the following environment variables (check `.env.example`):

* `FLASK_PORT` - Port number for the Flask application (e.g., `5000`)
* `FLASK_DEBUG` - Enable debug mode (`True` or `False`)
* `FLASK_ENV` - Application environment (`dev` or `prod`)
* `JWT_SECRET_KEY` - Secret key for signing JWT tokens
* `JWT_COOKIE_CSRF_PROTECT` - Enable CSRF protection on cookies (`True` or `False`)
* `JWT_COOKIE_SECURE` - Send cookies only over HTTPS (`True` for production, `False` for development)
* `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` - Access token expiration time in minutes (e.g., `15`)
* `JWT_REFRESH_TOKEN_EXPIRES_DAYS` - Refresh token expiration time in days (e.g., `30`)
* `POSTGRES_USER` - PostgreSQL username (e.g., `postgres`)
* `POSTGRES_PASSWORD`- PostgreSQL password
* `POSTGRES_HOST` - Host for PostgreSQL (e.g., `localhost` or a Docker Compose service name)
* `POSTGRES_PORT` - Port number for PostgreSQL (e.g., `5432`)
* `POSTGRES_DB` - PostgreSQL database name

You can customize these based on your local or production environment.

---

## 🧾 API Documentation

This backend provides the following main API groups:

- `/documents/*` - Upload, list, retrieve, and delete text documents  
- `/collections/*` - Create, manage, and associate documents with collections  
- `/users/*` - User registration, login, and token handling  
- `/system/*` - Runtime metrics and status  
- `/tfidf/*` - TF-IDF values calculations with a web interface
> ⚠️ Note: The web interface currently supports only a single document and exclusively TF analysis. Use the API for multi-document collection support with full TF-IDF statistics.

### 🧩️ API Endpoints

| Method   | URL                                          | Description                                                                                                        | Auth Required |
|----------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------|:-------------:|
| `GET`    | `/documents`                                 | Get all documents for the current user.                                                                            |       ✅       |
| `POST`   | `/documents`                                 | Upload a new `.txt` document.                                                                                      |       ✅       |
| `GET`    | `/documents/<document_id>`                   | Fetch contents of a specific document.                                                                             |       ✅       |
| `GET`    | `/documents/<document_id>/statistics`        | Get term frequency (TF) if the document is not in any collection; otherwise, return full TF-IDF stats.             |       ✅       |
| `DELETE` | `/documents/<document_id>`                   | Delete a specific document.                                                                                        |       ✅       |
| `GET`    | `/collections`                               | Get collections with documents in them for the current user.                                                       |       ✅       |
| `POST`   | `/collections`                               | Create a collection.                                                                                               |       ✅       |
| `GET`    | `/collections/<collection_id>`               | Fetch documents from specific collection.                                                                          |       ✅       |
| `GET`    | `/collections/<collection_id>/statistics`    | Get TF-IDF statistics for the collection.                                                                          |       ✅       |
| `POST`   | `/collections/<collection_id>/<document_id>` | Add a document to the collection.                                                                                  |       ✅       |
| `DELETE` | `/collections/<collection_id>/<document_id>` | Remove specific document from collection.                                                                          |       ✅       |
| `POST`   | `/users/login`                               | Authenticate a user.                                                                                               |       ❌       |
| `POST`   | `/users/register`                            | Register a new user.                                                                                               |       ❌       |
| `GET`    | `/users/logout`                              | Logout the current user.                                                                                           |       ✅       |
| `PATCH`  | `/users/<user_id>`                           | Update the password for the authenticated user.                                                                    |       ✅       |
| `DELETE` | `/users/<user_id>`                           | Delete the authenticated user and clear cookies.                                                                   |       ✅       |
| `POST`   | `/users/refresh`                             | Use refresh token to obtain a new access token.                                                                    |       ✅       |
| `GET`    | `/system/status`                             | Check if the system is running.                                                                                    |       ❌       |
| `GET`    | `/system/metrics`                            | Retrieve system usage metrics.                                                                                     |       ❌       |
| `GET`    | `/system/version`                            | Get the current version of the system.                                                                             |       ❌       |
| `GET`    | `/tfidf`                                     | Get the HTML template for uploading a single document.                                                             |       ❌       |
| `POST`   | `/tfidf`                                     | Retrieve an HTML page displaying a table of TF values only, as the document is not part of any collection for now. |       ❌       |

### 🧪 Interactive API Docs

You can explore and test all API endpoints directly via Swagger UI:

🔗 [Swagger UI Documentation](http://37.9.53.217/api/docs)

This interactive interface allows you to:
- View all available endpoints
- See input and output schemas
- Authenticate and test requests

---

## 🩹 App Version

The current app version is defined in `app/version.py`:

```python
__version__ = "0.2.0"
```

---

## 📓 Recent Changes

* New entities: documents, collections, users
* JWT integration

For a full list of changes, refer to the [CHANGELOG.md](./CHANGELOG.md).

---

## 📚 References

### 1. [TF-IDF — Wikipedia](https://ru.wikipedia.org/wiki/TF-IDF)

### 2. [Извлечение признаков из текстовых данных с использованием TF-IDF — Habr](https://habr.com/ru/companies/otus/articles/755772/)

### 3. [Understanding TF-IDF (Term Frequency-Inverse Document Frequency)](https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/)

### 4. [Two minutes NLP — Learn TF-IDF with easy examples](https://medium.com/nlplanet/two-minutes-nlp-learn-tf-idf-with-easy-examples-7c15957b4cb3)
