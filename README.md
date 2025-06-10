# Frequency Counter

A Flask-based backend that exposes endpoints for uploading .txt documents, organizing them into collections, and computing text statistics like TF-IDF. It also manages users and system metrics, with a minimal frontend included for basic interaction.

---

## 📁 Project Structure

```
freq_counter/
│
├── app/                          # Main Flask application package
│   |
│   ├── collections/              # Management of document groupings
│   │   ├── __init__.py                
│   │   ├── api_routes.py         # JSON API endpoints 
│   │   ├── decorators.py         # Decorators for validating collections before operating over them
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── routes.py             # Future HTML-rendering routes (currently not implemented)
│   │   └── services.py           # Business logic 
│   |
│   ├── documents/                # Handles document upload, processing, and metadata
│   │   ├── __init__.py
│   │   ├── api_routes.py         # JSON API endpoints 
│   │   ├── decorators.py         # Decorators for validating documents before operating over them
│   │   ├── error_handlers.py     # Custom error handlers 
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── routes.py             # Future HTML-rendering views (currently empty)
│   │   └── services.py           # Business logic 
│   |
│   ├── media/                    # Directory for storing uploaded text documents
│   |
│   ├── shared/                   # Shared helpers and base components
│   │   ├── __init__.py
│   │   ├── common_models.py      # Reusable SQLAlchemy models
│   │   ├── exceptions.py         # Custom exception classes
│   │   ├── file_utils.py         # Utility functions for validating files
│   │   └── tfidf_stats.py        # Helpers for calculating TF-IDF values
│   |
│   ├── system/                   # Tracks runtime metrics, logs, and app status
│   │   ├── __init__.py
│   │   ├── api_routes.py         # JSON endpoints for system health, metrics, logs
│   │   ├── models.py             # Models for system metrics information 
│   │   └── services.py           # Aggregates and computes metrics or status values
│   |
│   ├── templates/                # Jinja2 HTML templates (used in `routes.py`)
│   |
│   ├── tfidf/                    # Web interface for documents uploading (not fully implemented)
│   │   ├── __init__.py
│   │   ├── routes.py             # HTML endpoints for viewing TF-IDF results
│   │   └── services.py           # Business logic 
│   |
│   ├── users/                    # Authentication and user management
│   │   ├── __init__.py
│   │   ├── api_routes.py         # JSON endpoints for login, register, etc.
│   │   ├── decorators.py         # Decorators checking authorization
│   │   ├── models.py             # User related models
│   │   └── services.py           # Password hashing, token logic, etc.
│   |
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

---

## 🚀 How to Run the App
### 🐳 Using Docker

1. **Clone the repository**

   ```bash
   git clone https://github.com/AmalSultanov/freq_counter
   cd freq_counter
   ```

2. **Create a `.env` file and set environment variables in any editor**

   Refer to  [⚙️ Environment Variables](#%EF%B8%8F-environment-variables) section for  clarification.

   ```bash
   cp .env.example .env
   nano .env
   ```

3. **Build and run using Docker Compose**

   ```bash
   docker compose up --build
   ```

4. The app will be available at `http://127.0.0.1`.

---

## ⚙️ Environment Variables

The application uses the following environment variables (see `.env.example`):

* `FLASK_PORT` - Port number for the Flask application (e.g., `5000`)
* `FLASK_DEBUG` - Enable debug mode (`True` or `False`)
* `FLASK_ENV` - Application environment (`dev` or `prod`)
* `JWT_SECRET_KEY ` - Secret key for signing JWT tokens
* `JWT_COOKIE_CSRF_PROTECT ` - Enable CSRF protection on cookies (`True` or `False`)
* `JWT_COOKIE_SECURE ` - Send cookies only over HTTPS (`True` for production, `False` for development)
* `JWT_ACCESS_TOKEN_EXPIRES_MINUTES ` - Access token expiration time in minutes (e.g., `15`)
* `JWT_REFRESH_TOKEN_EXPIRES_DAYS ` - Refresh token expiration time in days (e.g., `30`)
* `POSTGRES_USER` - PostgreSQL username (e.g., `postgres`)
* `POSTGRES_PASSWORD`- PostgreSQL password
* `POSTGRES_HOST` - Host for PostgreSQL (e.g., `localhost` or a Docker Compose service name)
* `POSTGRES_PORT` - Port number for PostgreSQL (e.g., `5432`)
* `POSTGRES_DB` - PostgreSQL database name

You can customize these based on your local or production environment.

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
