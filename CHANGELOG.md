# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org).

---
## 0.2.0 - (2025-06-10)

### Added
- New core entities: `documents/`, `collections/`, and `users/` with corresponding endpoints, models and services to support API development
- `shared/` package to group reusable components and utilities
- Migrations to support newly introduced entities
- JWT-based authentication

### Changed
- Structure of `media/`: folders inside are named after usernames
- Rename `metrics/` to `system/` to reflect logs and system-level information
- Migrate from standard Flask routes to Flask-RESTX for better API structure, documentation, and Swagger support

### Fixed
- Duplicate documents now cannot be uploaded

---
## 0.1.1 - (2025-05-27)

### Added
- `tfidf/` package with endpoints and services for web interface
- `metrics/` package with endpoints, services and a single model for metrics tracking. The proposed metrics are:
  - `uploads_count_per_day` - number of uploaded documents within a day, helps to understand the daily load on the app
  - `largest_file_size_in_bytes` - the largest file size that was uploaded so far, can reflect the performance tendency of app in case of large document size
- `database.py` for SQLAlchemy setup 
- `version.py` to track the current app version
- `config.py` for centralized configuration management
- `.env` and `.env.example` files for environment variables management
- `migrations/` package for database schema migrations by Alembic
- Docker support with PostgreSQL and Nginx (`Dockerfile`, `docker-compose.yml`, `.dockerignore`)
- `CHANGELOG.md` for tracking project related updates
- Gunicorn support

### Changed
- `app/` package is now main application package
- Move `templates/` and `media/` folders inside `app/`
- Rename `app.py` to `run.py` and move app initialization to `app/__init__.py`

### Fixed
- Modularity was improved through better separation of concerns

---

## 0.1.0 - (2025-04-24)
_First release._
