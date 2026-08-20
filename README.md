# TaskManagerAPI

A production‑ready REST API for managing tasks with JWT authentication, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User registration & login (JWT)
- Full CRUD for tasks (with ownership)
- Filtering, pagination, sorting
- OpenAPI docs at `/api/docs`
- Containerised with Docker
- Comprehensive test suite (>90% coverage)
- CI with linting, type checking, and tests

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and set `DATABASE_URL` and `SECRET_KEY`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
# TaskManagerAPI
