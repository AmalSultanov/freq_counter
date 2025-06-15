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
* [Generating a Python API Client](#-generating-a-python-api-client)
* [App Version](#-app-version)
* [Recent Changes](#-recent-changes)
* [References](#-references)

---

## 📁 Project Structure

```
freq_counter/
│
├── api_client/                   # Directory for API client library generation
│   └── swagger.yaml              # OpenAPI specification
│
├── app/                          # Main Flask application package
│   │
│   ├── admin/                    # Administering using Flask-Admin
│   │   ├── views/                # Views to display admin page, models, etc
│   │   ├── __init__.py                
│   │   ├── decorators.py         # Decorators for validating access rights
│   │   ├── routes.py             # Auth and admin dashboard routes
│   │   └── services.py           # Business logic 
│   │
│   ├── collections/              # Management of document groupings
│   │   ├── services/             # Existence checks, CRUD, etc.               
│   │   ├── __init__.py                
│   │   ├── api_models.py         # API schema definitions
│   │   ├── api_routes.py         # JSON API endpoints 
│   │   ├── decorators.py         # Decorators for validating collections before operating over them
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── namespace.py          # Namespace registration, like a blueprint
│   │   ├── routes.py             # Placeholder for future web views
│   │   └── selectors.py          # Business logic (getter functions) 
│   │
│   ├── documents/                # Handles document upload, processing, and metadata
│   │   ├── services/             # Existence checks, CRUD, etc.
│   │   ├── __init__.py
│   │   ├── api_models.py         # API schema definitions 
│   │   ├── api_routes.py         # JSON API endpoints 
│   │   ├── decorators.py         # Decorators for validating documents before operating over them
│   │   ├── error_handlers.py     # Custom error handlers 
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── namespace.py          # Namespace registration, like a blueprint
│   │   ├── routes.py             # Placeholder for future web views
│   │   └── selectors.py          # Business logic (getter functions) 
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
│   ├── extensions.py             # Declaration of JWTManager, Cache, etc.
│   └── version.py                # App version info
│
├── migrations/                   # Alembic migrations
├── nginx/                        # Nginx related configurations
├── .dockerignore                 
├── .env                          
├── .env.example                  # Sample .env
├── .gitignore                    
├── CHANGELOG.md                  # Leave your feedback here in designated section
├── docker-compose.yml            
├── Dockerfile                     
├── README.md                     
├── requirements.txt              
└── run.py                        
```

---

## 🖼️ Entities Involved



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
* `CACHE_REDIS_HOST` - Host for Redis (e.g, `localhost` or a Docker Compose service name)
* `CACHE_REDIS_PORT` - Port number for Redis to run on
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
> ⚠️ Note: The web interface currently supports only a single document and exclusively TF analysis (still under development). Use the API for multi-document collection support with full TF-IDF statistics.

### 🧩️ API Endpoints

### Documents

| Method   | URL                                          | Description                                                                                                        | Auth Required |
|----------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------|:-------------:|
| `GET`    | `/documents`                                 | Get all documents for the current user.                                                                            |       ✅       |
| `POST`   | `/documents`                                 | Upload a new `.txt` document.                                                                                      |       ✅       |
| `GET`    | `/documents/<document_id>`                   | Fetch contents of a specific document.                                                                             |       ✅       |
| `GET`    | `/documents/<document_id>/statistics`        | Get term frequency (TF) if the document is not in any collection; otherwise, return full TF-IDF stats.             |       ✅       |
| `GET`    | `/documents/<document_id>/huffman`           | Fetch contents of a specific document and encode it into Huffman coded form.                                       |       ✅       |
| `DELETE` | `/documents/<document_id>`                   | Delete a specific document.                                                                                        |       ✅       |


### Collections

| Method   | URL                                          | Description                                                                                                        | Auth Required |
|----------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------|:-------------:|
| `GET`    | `/collections`                               | Get collections with documents in them for the current user.                                                       |       ✅       |
| `POST`   | `/collections`                               | Create a collection.                                                                                               |       ✅       |
| `GET`    | `/collections/<collection_id>`               | Fetch documents from specific collection.                                                                          |       ✅       |
| `GET`    | `/collections/<collection_id>/statistics`    | Get TF-IDF statistics for the collection.                                                                          |       ✅       |
| `POST`   | `/collections/<collection_id>/<document_id>` | Add a document to the collection.                                                                                  |       ✅       |
| `DELETE` | `/collections/<collection_id>/<document_id>` | Remove specific document from collection.                                                                          |       ✅       |

### Users

| Method   | URL                                          | Description                                                                                                        | Auth Required |
|----------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------|:-------------:|
| `POST`   | `/users/login`                               | Authenticate a user.                                                                                               |       ❌       |
| `POST`   | `/users/register`                            | Register a new user.                                                                                               |       ❌       |
| `GET`    | `/users/logout`                              | Logout the current user.                                                                                           |       ✅       |
| `PATCH`  | `/users/<user_id>`                           | Update the password for the authenticated user.                                                                    |       ✅       |
| `DELETE` | `/users/<user_id>`                           | Delete the authenticated user and clear cookies.                                                                   |       ✅       |
| `POST`   | `/users/refresh`                             | Use refresh token to obtain a new access token.                                                                    |       ✅       |

### System

| Method   | URL                                          | Description                                                                                                        | Auth Required |
|----------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------|:-------------:|
| `GET`    | `/system/status`                             | Check if the system is running.                                                                                    |       ❌       |
| `GET`    | `/system/metrics`                            | Retrieve system usage metrics.                                                                                     |       ❌       |
| `GET`    | `/system/version`                            | Get the current version of the system.                                                                             |       ❌       |

### 🧪 Interactive API Docs

Explore and test all API endpoints directly via Swagger UI:

🔗 [Swagger UI Documentation](http://37.9.53.217/api/docs)

This interactive interface allows you to:
- View all available endpoints
- See input and output schemas
- Authenticate and test requests

> Do not forget to click `Authorize` and paste the access token in form `Bearer access_token` right after you register an account or log into existing one. 

---

## 🛠️ Generating a Python API Client

You can generate a Python API client using the [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client) generator, based on the OpenAPI specification located at `api_client/swagger.yaml`.
> ✅ This tool is already installed as part of the project dependencies.

### 📤️ Generate the Client

Run the following command from the project root to generate or update the API client package:

```bash
openapi-python-client generate --path api_client/swagger.yaml --output-path api_client --overwrite
```

This will generate the client code in the `api_client` directory.

### 🧪 Example Usage

Create a python file (e.g. `main.py`) and a random text file (e.g. `test.txt`) inside `api_client` directory, at the same level as the `swagger.yaml`. The `main.py` script below sends a request to upload a document and prints the response:

```python 
import word_frequency_counter_tf_idf_analyzer_api_client.api.documents.post_documents_list_resource as upload
from word_frequency_counter_tf_idf_analyzer_api_client.models.post_documents_list_resource_body import PostDocumentsListResourceBody
from word_frequency_counter_tf_idf_analyzer_api_client.types import File
from word_frequency_counter_tf_idf_analyzer_api_client import AuthenticatedClient


def print_result(filename):
    client = AuthenticatedClient(
        base_url="http://127.0.0.1",  # Replace with your actual server address
        token="token",                # Replace with your valid access token
    )

    with open(filename, "rb") as f:
        file_data = File(payload=f, file_name=filename, mime_type="text/plain")
        data = PostDocumentsListResourceBody(file=file_data)
        result = upload.sync(client=client, body=data)
        print(result)


if __name__ == "__main__":
    print_result("test.txt")
```

> 🔐 You can obtain your token by registering or logging in through the Swagger UI Documentation.

Sample output responses of this script:

#### ✅ Successful Upload
```bash
Message(message='Document with id = 4 was uploaded', additional_properties={})
```

#### ⚠️ Duplicate Document    
```bash
Message(message='Document with this content was already uploaded earlier', additional_properties={})
```

#### ⚠️ Empty File Submission
```bash
Message(message='Uploading empty files is not allowed', additional_properties={})
```

#### 🚫 File Too Large   
```bash
Message(message='The data value transmitted exceeds the capacity limit.', additional_properties={})
```

#### ❌ Invalid File Type
```bash
Message(message='Only .txt files are allowed', additional_properties={})
```

---

## 🩹 App Version

The current app version is defined in `app/version.py`:

```python
__version__ = "1.2.0"
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
