# API Reference

## Authentication

### POST /api/auth/register
Register a new user.

**Request body**:
```json
{
  "email": "user@example.com",
  "password": "StrongPass1",
  "full_name": "John Doe"
}#!/bin/bash

# ----------------------------------------------------------------------------
# 1. Define the project root directory
# ----------------------------------------------------------------------------
PROJECT_NAME="TaskManagerAPI"
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME" || exit

# ----------------------------------------------------------------------------
# 2. Create directory structure
# ----------------------------------------------------------------------------
mkdir -p src/repositories src/services src/routers tests docs .github/workflows

# ----------------------------------------------------------------------------
# 3. Write all files (heredoc style)
# ----------------------------------------------------------------------------

# --- .github/workflows/ci.yml ---
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff mypy pytest-cov

      - name: Lint with ruff
        run: ruff check src/ tests/

      - name: Type check with mypy
        run: mypy src/

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
          SECRET_KEY: testsecret
        run: |
          pytest --cov=src --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov (optional)
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: unittests
