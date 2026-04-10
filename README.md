# 📣 FastAPI Social Platform

A robust and scalable **social platform** built with **FastAPI** and powered by **PostgreSQL**, where users can **share content** and **vote** on posts. This project demonstrates modern backend development practices, with full support for **Docker** to ensure seamless deployment across environments.

---

## Features

- **FastAPI Framework** – High-performance Python web framework with automatic OpenAPI docs and blazing-fast async support.
- **PostgreSQL Integration** – Reliable relational database for structured data storage, complex queries, and ACID-compliant transactions.
- **Docker Support** – Fully containerized setup with `Dockerfile` and `docker-compose` for consistent, one-command deployment.
- **Full CRUD Operations** – Complete Create, Read, Update, and Delete functionality for posts and users.
- **Voting System** – Users can upvote or downvote posts, with vote counts tracked per post.
- **User Authentication** – Secure JWT-based auth so only registered users can post and vote.
- **Input Validation** – Automatic request/response validation powered by Pydantic v2 models.
- **Auto-Generated API Docs** – Interactive Swagger UI and ReDoc documentation available out of the box.

---

## 🚀 Live Demo

The API is live and deployed on **Render**. Explore the interactive documentation without any setup:

| | Link |
|---|---|
| **Swagger UI** | [https://fastapi-management-system.onrender.com/docs](https://fastapi-management-system.onrender.com/docs) |
| **ReDoc** | [https://fastapi-management-system.onrender.com/redoc](https://fastapi-management-system.onrender.com/redoc) |
| **Base URL** | [https://fastapi-management-system.onrender.com](https://fastapi-management-system.onrender.com) |

> ⚠️ **Note:** The service may take **30–60 seconds** to wake up on first load, as it runs on Render's free tier.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI (Python 3.9+) |
| **Database** | PostgreSQL 15 |
| **Validation** | Pydantic v2 |
| **Authentication** | JWT (python-jose) |
| **Migrations** | Alembic |
| **Containerization** | Docker + Docker Compose |
| **Hosting** | Render |

---

## How It Works

1. **Register** a new account or **log in** to get a JWT access token.
2. **Create posts** to share content with the community.
3. **Browse posts** from other users.
4. **Vote** on posts you like or dislike.
5. **Manage your posts** — edit or delete anything you've created.

---

## Getting Started

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) (locally or remotely accessible)
- [Docker](https://www.docker.com/get-started/) *(optional, for containerized deployment)*
- [Git](https://git-scm.com/)

---

### Installation (Local)

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/FastAPI-Social-Platform.git
cd FastAPI-Social-Platform
```

**2. Create and activate a virtual environment:**

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**3. Install all dependencies:**

```bash
pip install -r requirements.txt
```

**4. Configure your environment variables:**

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Then update the values in `.env`:

```env
# Database
database_hostname=localhost
database_port=5432
database_username=postgres
database_password=postgres
database_name=fastapi

# Auth / JWT
secret_key=CHANGE_ME
algorithm=HS256
access_token_expire_minutes=60

# CORS
cors_origins=*
```

**5. Run database migrations:**

```bash
alembic upgrade head
```

**6. Start the development server:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Base URL:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

### 🐳 Installation (Docker)

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/FastAPI-Social-Platform.git
cd FastAPI-Social-Platform
```

**2. Configure your environment:**

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

**3. Build and run with Docker Compose:**

```bash
docker-compose up --build
```

This will spin up both the FastAPI app and a PostgreSQL container. The API will be accessible at `http://localhost:8000`.

To run in detached mode:

```bash
docker-compose up --build -d
```

To stop the containers:

```bash
docker-compose down
```

---

## 📡 API Endpoints Overview

### 👤 Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login` | Log in and receive a JWT token |

### 👥 Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Register a new user |
| `GET` | `/users/{id}` | Get a user's profile |

### 📝 Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/posts/` | Browse all posts |
| `POST` | `/posts/` | Share a new post |
| `GET` | `/posts/{id}` | View a single post |
| `PUT` | `/posts/{id}` | Edit your post |
| `DELETE` | `/posts/{id}` | Delete your post |

### 👍 Votes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/vote/` | Upvote or remove your vote on a post |

> 🔐 Most endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.
>
> Full interactive documentation available at [`/docs`](https://fastapi-management-system.onrender.com/docs).

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📬 Contact

Have questions or suggestions? Open an issue or reach out via GitHub Discussions.

---

<p align="center">Built with ❤️ using FastAPI & PostgreSQL</p>

![giphy](https://github.com/user-attachments/assets/f3bb48f1-537c-4323-be64-9c4e02268191)

