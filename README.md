#  FastAPI Management System

A robust and scalable **management system** built with **FastAPI** and powered by **PostgreSQL**. This project demonstrates modern backend development practices, with full support for **Docker** to ensure seamless deployment across environments.

---

##  Features

-  **FastAPI Framework** – High-performance Python web framework with automatic OpenAPI docs and blazing-fast async support.
- **PostgreSQL Integration** – Reliable relational database for structured data storage, complex queries, and ACID-compliant transactions.
-  **Docker Support** – Fully containerized setup with `Dockerfile` and `docker-compose` for consistent, one-command deployment.
- **Full CRUD Operations** – Complete Create, Read, Update, and Delete functionality for all resource types.
-  **Input Validation** – Automatic request/response validation powered by Pydantic v2 models.
-  **Auto-Generated API Docs** – Interactive Swagger UI and ReDoc documentation available out of the box.


---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI (Python 3.9+) |
| **Database** | PostgreSQL 15 |
| **Validation** | Pydantic v2 |
| **Containerization** | Docker + Docker Compose |


---



---

##  Getting Started

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) (locally or remotely accessible)
- [Docker](https://www.docker.com/get-started/) *(optional, for containerized deployment)*
- [Git](https://git-scm.com/)

---

###  Installation (Local)

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/FastAPI-Management-System.git
cd FastAPI-Management-System
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
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# App
APP_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000
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
git clone https://github.com/your-username/FastAPI-Management-System.git
cd FastAPI-Management-System
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

##  Running Tests

Make sure your virtual environment is active, then run:

Fast Api swegger

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` |  check all the contants |
| `GET` | `/posts` | List all posts |
| `POST` | `/posts` | Create a new  post |
| `GET` | `/posts/{id}` | Get a single post |
| `PUT` | `/posts/{id}` | Update an post |
| `DELETE` | `/posts/{id}` | Delete an post|

> Full interactive documentation is available at `/docs` when the server is running.

---

##  Contributing

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

