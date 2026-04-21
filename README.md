# Premium E-Commerce Platform

A robust, secure, and modern e-commerce solution built with FastAPI and a premium Vanilla JS frontend.

## 🚀 Features

- **Secure Authentication**: JWT-based auth with access and refresh tokens.
- **Role-Based Access Control (RBAC)**: Distinct permissions for Admins and Users.
- **Premium Frontend**: Amazon-level design aesthetics using modern CSS and Vanilla JS.
- **Modular Backend**: Clean architecture with core, api, models, schemas, repositories, and services.
- **Docker Ready**: Fully containerized with Docker and Docker Compose.
- **Validated**: Comprehensive test suite using Pytest.

## 🛠️ Tech Stack

- **Backend**: Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, MySQL/SQLite.
- **Frontend**: HTML5, CSS3 (Custom Design System), JavaScript (ES6+).
- **Infrastructure**: Docker, Redis (Caching), MySQL.

## 📥 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.13 (for local development)

### 2. Configuration
Copy the `.env.example` to `.env` and update the values:
```bash
cp ecommerce-backend/.env.example ecommerce-backend/.env
```

### 3. Running with Docker (Recommended)
```bash
docker-compose up -d
```
The API will be available at `http://localhost:8000` and the documentation at `http://localhost:8000/docs`.

### 4. Local Development
```bash
cd ecommerce-backend
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 5. Running Tests
```bash
cd ecommerce-backend
pytest
```

### 6. Create Admin User
```bash
python ecommerce-backend/scripts/create_admin.py
```

## 📂 Project Structure

```text
├── ecommerce-backend/       # Backend FastAPI application
│   ├── app/                 # Main application logic
│   ├── alembic/             # Database migrations
│   ├── scripts/             # Utility scripts (create_admin.py)
│   ├── tests/               # Pytest suite
│   └── Dockerfile           # Backend containerization
├── frontend/                # Premium Vanilla JS frontend
│   ├── css/                 # Custom design system
│   ├── js/                  # API and page logic
│   └── *.html               # Premium page templates
└── docker-compose.yml       # Full stack orchestration
```

## 🛡️ Security
- Password hashing using `bcrypt`.
- JWT tokens with `JOSE`.
- Protected routes via FastAPI dependencies.

## 📄 License
MIT