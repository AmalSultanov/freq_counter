# Frequency Counter

A Python web application that processes uploaded `.txt` files and computes the  TF-IDF (Term Frequency–Inverse Document Frequency) scores for the words in the  document.

---

## 📁 Project Structure

```
freq_counter/
│
├── app/                         # main application package
│   ├── media/                   # uploaded text files
│   ├── metrics/                 # metrics models, routes, and services
│   ├── templates/               # HTML templates
│   ├── tfidf/                    # TF-IDF routes and services
│   ├── __init__.py              # app factory initialization
│   ├── config.py                 # Base, Development and Production configurations
│   ├── database.py              # SQLAlchemy setup
│   └── version.py               # app versioning
│
├── migrations/                  # Alembic migration scripts
├── .dockerignore                
├── .env                         
├── .env.example                 # example env file for reference
├── .gitignore                   
├── CHANGELOG.md                 
├── docker-compose.yml           
├── Dockerfile                    
├── nginx.template.conf          # configurations for Nginx       
├── README.md                    
├── requirements.txt             
└── run.py                       # entry point for running the app
```

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

* `FLASK_PORT` - port number for Flask application, for example 5000
* `FLASK_DEBUG` - debug value, True or False
* `FLASK_ENV` - environment value, 'dev' or 'prod'
* `POSTGRES_USER` - user for postgres, for example 'postgres'
* `POSTGRES_PASSWORD`- password for postgres
* `POSTGRES_HOST` - postgres host, for example 'localhost' or service name of PostgreSQL container if using Docker Compose
* `POSTGRES_PORT` - port number for postgres, for example 5432
* `POSTGRES_DB` - postgres database name

You can customize these based on your local or production environment.

---

## 🩹 App Version

The current app version is defined in `app/version.py`:

```python
__version__ = "0.1.1"
```

---

## 📓 Recent Changes

* Major project changes include refactoring and modularization.
* Docker support, PostgreSQL, Nginx and Gunicorn integration.
* Configurations and migrations management as well as version tracking.

For a full list of changes, refer to the [CHANGELOG.md](./CHANGELOG.md).

---

## 📚 References

### 1. [TF-IDF — Wikipedia](https://ru.wikipedia.org/wiki/TF-IDF)

### 2. [Извлечение признаков из текстовых данных с использованием TF-IDF — Habr](https://habr.com/ru/companies/otus/articles/755772/)

### 3. [Understanding TF-IDF (Term Frequency-Inverse Document Frequency)](https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/)

### 4. [Two minutes NLP — Learn TF-IDF with easy examples](https://medium.com/nlplanet/two-minutes-nlp-learn-tf-idf-with-easy-examples-7c15957b4cb3)