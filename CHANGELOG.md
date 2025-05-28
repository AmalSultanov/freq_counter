# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org).

---

## 0.1.1 - (2025-05-27)
### Added
- `tfidf/` package with route handlers and services inside `app/`.
- `metrics/` package with route handlers, services and a single model for metrics tracking inside `app/`.
- `database.py` for handling SQLAlchemy connection setup inside `app/`.
- `version.py` inside `app/` to track the current app version.
- `config.py` inside `app/` for centralized configuration management.
- `.env` and `.env.example` files for environment variables management.
- `migrations/` package for database schema migrations by Alembic.
- Docker support (`Dockerfile`, `docker-compose.yml`) to containerize the app and PostgreSQL.
- `CHANGELOG.md` for tracking project related updates.
- `.dockerignore`.

### Changed
- Project structure:
  - Create `app/` package as main application package.
  - Move `templates/` and `media/` folders inside `app/`.
  - Rename `app.py` to `run.py` and move app initialization to `app/__init__.py`.

### Fixed
- Improved modularity through better separation of concerns.

---

## 0.1.0 - (2025-04-24)
_First release._
