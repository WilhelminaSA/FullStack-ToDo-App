# Full-Stack To-Do Application

A full-stack task management application built with **React** and **Flask**, featuring JWT authentication, role-based access control, task management, and an admin dashboard.

The application has two user roles:

* **Regular User** - Manage their own tasks
* **Admin** - Manage users and view/manage all tasks

---

## Project Overview

This project demonstrates a complete full-stack application with:

* React frontend
* Flask REST API backend
* SQLAlchemy ORM
* SQLite database for local development
* JWT-based authentication
* Role-based authorization
* User and task management
* Admin dashboard
* Protected frontend routes
* API integration between React and Flask
* Automated backend and frontend tests

---

## Key Features

### User Features

* User registration
* User login
* JWT authentication
* Create tasks
* View personal tasks
* Update tasks
* Delete tasks
* Mark tasks as completed/uncompleted
* Filter tasks by completion status
* Filter tasks by priority
* Set task priority
* Set task due dates
* Persistent authentication after page refresh

### Admin Features

* Dedicated admin login
* JWT-based admin authentication
* Role-based authorization
* View all registered users
* Search users
* Update usernames and email addresses
* Change user roles
* Activate/deactivate user accounts
* Delete users
* View all tasks
* Search and filter tasks
* Delete tasks
* Admin statistics dashboard

---

## Technology Stack

### Frontend

* React
* JavaScript
* Vite
* React Router
* CSS
* Vitest
* React Testing Library

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* PyJWT
* Werkzeug
* Flask-CORS

### Database

* SQLite for local development
* SQLAlchemy ORM

### Testing

* Pytest for backend
* Vitest + React Testing Library for frontend

---

## Architecture

The application follows a frontend-backend architecture:

```text
                    React Frontend
                         |
                         | HTTP / REST API
                         |
                         v
                  Flask Backend
                         |
              +----------+----------+
              |                     |
        JWT Authentication      RBAC
              |                     |
              +----------+----------+
                         |
                    SQLAlchemy
                         |
                         v
                    SQLite DB
```

### Request Flow

```text
User
  |
  v
React UI
  |
  v
API Layer
  |
  | JWT Bearer Token
  v
Flask REST API
  |
  +--> Authentication / Authorization
  |
  +--> Task Operations
  |
  +--> Admin Operations
  |
  v
SQLAlchemy
  |
  v
Database
```

For a detailed explanation of the architecture, see:

* [Architecture Documentation](ARCHITECTURE.md)
* [API Documentation](API_DOCUMENTATION.md)
* [Feature List](features.md)

---

## Project Structure

```text
ToDo_Flask_Backend/
│
├── app.py
├── models.py
├── admin.py
├── requirements.txt
├── .gitignore
│
├── routes/
│   ├── __init__.py
│   └── auth.py
│
├── utils/
│   ├── __init__.py
│   └── security.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_admin.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── tests/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── API_DOCUMENTATION.md
├── ARCHITECTURE.md
├── README.md
└── features.md
```

---

## Authentication

The application uses **JWT (JSON Web Tokens)** for authentication.

### User Authentication

Users can:

1. Register using `/signup`
2. Log in using `/login`
3. Receive an authentication token
4. Use the token when accessing protected task endpoints

Authenticated requests use:

```text
Authorization: Bearer <token>
```

### Admin Authentication

Admins use a dedicated endpoint:

```text
POST /admin/login
```

The backend verifies:

* Email
* Password
* Account status
* User role

Only users with the `admin` role can access admin-protected endpoints.

---

## Role-Based Access Control

The application uses two roles:

```text
user
admin
```

Administrators are modeled as normal users with an elevated role rather than using a separate administrator table.

This allows authentication to remain consistent while authorization determines which resources and operations each user can access.

### User Permissions

Regular users can:

* Manage their own tasks
* View only their own tasks
* Update their own tasks
* Delete their own tasks

### Admin Permissions

Admins can:

* Manage users
* Change user roles
* Activate/deactivate users
* Delete users
* View all tasks
* Delete tasks belonging to any user

---

## API Endpoints

### General

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| GET    | `/`      | API welcome message |

### Authentication

| Method | Endpoint  | Description         |
| ------ | --------- | ------------------- |
| POST   | `/signup` | Register a new user |
| POST   | `/login`  | Authenticate a user |

### User Tasks

| Method | Endpoint      | Description              |
| ------ | ------------- | ------------------------ |
| POST   | `/tasks`      | Create a task            |
| GET    | `/tasks`      | Get current user's tasks |
| GET    | `/tasks/<id>` | Get a specific task      |
| PUT    | `/tasks/<id>` | Update a task            |
| DELETE | `/tasks/<id>` | Delete a task            |

### Admin

| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| POST   | `/admin/login`      | Authenticate an admin |
| GET    | `/admin/users`      | Get all users         |
| PUT    | `/admin/users/<id>` | Update a user         |
| DELETE | `/admin/users/<id>` | Delete a user         |
| GET    | `/admin/tasks`      | Get all tasks         |

For request bodies, authentication requirements, validation rules, and response formats, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

---

## Database Design

The application uses two primary tables:

### User

```text
User
├── id
├── username
├── email
├── password_hash
├── role
├── is_active
└── created_at
```

### Task

```text
Task
├── id
├── user_id
├── title
├── description
├── priority
├── completed
├── due_date
└── created_at
```

Relationship:

```text
User 1 ──────────── * Task
```

One user can have multiple tasks.

Each task belongs to exactly one user through the `user_id` foreign key.

---

## Task Fields

Each task supports:

* **Title**
* **Description**
* **Priority**

  * Low
  * Medium
  * High
* **Completed status**
* **Due date**
* **Creation timestamp**

---

## Running the Backend

### 1. Clone the repository

```bash
git clone https://github.com/WilhelminaSA/ToDo_Flask_Backend.git
cd ToDo_Flask_Backend
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key_here
```

Do not commit the `.env` file to GitHub.

The repository already includes `.gitignore` rules to prevent environment files from being committed.

### 5. Start Flask

```powershell
python app.py
```

The backend runs on:

```text
http://127.0.0.1:5000
```

---

## Running the Frontend

Open another terminal and navigate to the frontend:

```powershell
cd frontend
```

### 1. Install dependencies

```powershell
npm install
```

### 2. Configure the API URL

Create:

```text
frontend/.env
```

with:

```env
VITE_API_URL=http://127.0.0.1:5000
```

### 3. Start the development server

```powershell
npm run dev
```

The frontend runs on the Vite development server, normally:

```text
http://localhost:5173
```

---

## Testing

### Backend Tests

From the project root:

```powershell
pytest
```

The backend test suite covers:

* Authentication
* User registration/login
* Task CRUD
* Task ownership
* Input validation
* Admin authentication
* Admin authorization
* User management
* Admin task management

### Frontend Tests

From the `frontend` directory:

```powershell
npm test
```

The frontend tests cover:

* API functions
* Authentication context
* Application routing
* Protected user routes
* Protected admin routes

The current project checkpoint has:

* **55 backend tests passing**
* **13 frontend tests passing**

---

## Security

The application implements several security practices:

* Password hashing using Werkzeug
* JWT authentication
* Role-based authorization
* Protected API endpoints
* Task ownership checks
* Admin-only endpoints
* Active/inactive account checks
* Environment-based secret key
* CORS configuration
* Sensitive `.env` files excluded from Git

---

## Documentation

Additional project documentation:

* [Feature List](features.md)
* [API Documentation](API_DOCUMENTATION.md)
* [Architecture Documentation](ARCHITECTURE.md)

---

## Screenshots

Screenshots of the application will be added here.

### User Login

*Add screenshot here.*

### User Dashboard

*Add screenshot here.*

### Admin Login

*Add screenshot here.*

### Admin Dashboard

*Add screenshot here.*

---

## Future Improvements

Possible future improvements include:

* Production deployment
* PostgreSQL production database
* Database migrations using Alembic/Flask-Migrate
* Refresh token support
* Password reset functionality
* Pagination for large task/user lists
* More comprehensive frontend component tests
* CI/CD using GitHub Actions
* Production environment configuration

---

## License

This project was built for educational and portfolio purposes.
