# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org).

---
## 0.1.1 - (2025-05-27)
### Added
- `tfidf/` package with endpoints and services inside `app/`
- `metrics/` package with endpoints, services and a single model for metrics tracking inside `app/`. The proposed metrics are:
  - `uploads_count_per_day` - number of uploaded documents within a day, helps to understand the daily load on the app
  - `largest_file_size_in_bytes` - the largest file size that was uploaded so far, can reflect the performance tendency of app in case of large document size
- `database.py` for handling SQLAlchemy connection setup inside `app/`
- `version.py` inside `app/` to track the current app version
- `config.py` inside `app/` for centralized configuration management
- `.env` and `.env.example` files for environment variables management
- `migrations/` package for database schema migrations by Alembic
- Docker support (`Dockerfile`, `docker-compose.yml`) to containerize the app, PostgreSQL and Nginx
- `CHANGELOG.md` for tracking project related updates
- `.dockerignore`
- Gunicorn support

### Changed
- `app/` package is now main application package
- Move `templates/` and `media/` folders inside `app/`
- Rename `app.py` to `run.py` and move app initialization to `app/__init__.py`

### Fixed
- Improved modularity through better separation of concerns

---

## 0.1.0 - (2025-04-24)
_First release._
