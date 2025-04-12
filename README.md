# 🏡 FineNest Django Server

This is the backend server for the FineNest project — a Django-based API used to handle OCR receipt uploads and structured data extraction (Hebrew support included).

The project runs inside Docker and connects to a PostgreSQL database container.

---

## 🐳 Prerequisites

- Docker & Docker Compose installed
- Python dependencies are managed inside the Docker container
- Project files live inside the `django_server/` folder

---

## 🚀 Getting Started

### 1. Build Everything

If this is your first time (or after making changes to dependencies):

```bash
docker compose build
```

### 2. Start PostgreSQL

```bash
docker compose up -d db
```

### 3. Run Django Server

Start the development server:

```bash
docker compose run --service-ports web python manage.py runserver 0.0.0.0:8000
```

## 🧠 Visit: http://localhost:8000

### 🛠 First-Time Setup

---

After project creation, run this once to set up the database tables:

```
docker compose run web python manage.py migrate
```

---

### 📂 Project Structure

```
server/
├── django_server/      # All Django code lives here
│   ├── manage.py
│   └── core/           # Main Django app
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

### 🧼 Cleanup

To stop and remove containers:

```
docker compose down
```

To clean up unused/temporary containers:

```
docker container prune
```
