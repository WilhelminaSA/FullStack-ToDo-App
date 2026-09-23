# Full-Stack To-Do Application

A full-stack To-Do application built with **React** and **Flask**, featuring JWT authentication, role-based access control, task management, and a dedicated admin dashboard.

The project demonstrates how a React frontend communicates with a Flask REST API backed by a relational database.

---

## Project Overview

This application provides two types of users:

* **Normal users** can manage their own tasks.
* **Administrators** can manage users and view/manage tasks across the application.

The application follows a client-server architecture:

```text
React Frontend
      │
      │ HTTP / JSON + JWT
      ▼
Flask REST API
      │
      │ SQLAlchemy
      ▼
Relational Database
```

The frontend handles the user interface and client-side state, while the backend is responsible for authentication, authorization, validation, business logic, and database operations.

---

# Key Features

## User Features

* User registration
* User login and logout
* JWT-based authentication
* Persistent login using browser storage
* Protected user dashboard
* Role-aware frontend routing

## Task Management

Authenticated users can:

* Create tasks
* View their own tasks
* Update tasks
* Delete tasks
* Mark tasks as completed/uncompleted
* Add task descriptions
* Set task priorities
* Set due dates

### Task Priorities

Tasks support three priority levels:

* Low
* Medium
* High

The default priority is **Medium**.

### Due Dates

Tasks can optionally have a due date using the:

```text
YYYY-MM-DD
```

format.

## Task Filtering

Users can filter their tasks by:

* Completion status
* Priority

Filters can be combined to quickly find relevant tasks.

## User Dashboard

The dashboard provides:

* Task list
* Task statistics
* Task creation and editing
* Task completion controls
* Filters
* Loading states
* Error states
* Empty states

---

# Admin Features

Administrators use a separate admin interface.

Administrators are represented using the same `User` model as normal users, with elevated permissions through:

```text
role = admin
```

## Admin Authentication

Administrators have a dedicated login endpoint and login page.

Admin authentication verifies:

* User credentials
* Account status
* Admin role

## Admin Dashboard

The admin dashboard provides an overview of:

* Total users
* Active users
* Number of administrators
* Total tasks
* Completed tasks

## User Management

Administrators can:

* View users
* Search users
* Update usernames
* Update email addresses
* Change user roles
* Activate/deactivate accounts
* Delete users

An administrator cannot delete their own currently authenticated account.

## Task Management

Administrators can:

* View tasks across the application
* See task ownership
* Search/filter tasks through the admin interface
* Delete tasks when required

Unlike normal users, administrators are not restricted to their own tasks.

---

# Authentication & Authorization

## JWT Authentication

The application uses JSON Web Tokens for authentication.

After successful login, the backend generates a JWT token.

The frontend sends the token with protected requests using:

```text
Authorization: Bearer <token>
```

Protected backend endpoints validate the token before processing the request.

## Role-Based Access Control

The application supports two roles:

```text
user
admin
```

### User

A normal user can:

* Manage their own tasks
* Access the user dashboard
* Use user-level APIs

### Admin

An administrator can:

* Access the admin dashboard
* Manage users
* Manage application-wide tasks
* Perform administrative operations

Authorization is enforced by the **backend**, not just by the React frontend.

## Task Ownership

Every task contains a `user_id` identifying its owner.

For normal users, the backend verifies that the requested task belongs to the authenticated user before allowing operations such as:

* View
* Update
* Delete

This prevents users from accessing another user's tasks by simply changing a task ID in an API request.

---

# Security

The application includes several security measures:

* Password hashing
* JWT authentication
* Protected API routes
* Role-based authorization
* Task ownership checks
* Disabled-account checks
* Backend-side input validation
* Admin authorization
* Admin self-deletion protection
* Environment-based secret configuration
* `.env` excluded from Git
* Database files excluded from Git

Passwords are never stored as plain text.

The application stores password hashes and verifies passwords against those hashes during authentication.

---

# Tech Stack

## Frontend

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| React                 | User interface            |
| React Router          | Client-side routing       |
| React Context         | Authentication state      |
| JavaScript            | Frontend development      |
| Vite                  | Development/build tooling |
| CSS                   | Styling                   |
| Vitest                | Frontend testing          |
| React Testing Library | UI testing                |

## Backend

| Technology       | Purpose                    |
| ---------------- | -------------------------- |
| Python           | Backend development        |
| Flask            | REST API                   |
| Flask-SQLAlchemy | Database ORM               |
| SQLAlchemy       | Database interaction       |
| PyJWT            | JWT authentication         |
| Werkzeug         | Password hashing           |
| Flask-CORS       | Cross-origin communication |
| python-dotenv    | Environment configuration  |
| Pytest           | Backend testing            |

## Database

* SQLite for local development
* SQLAlchemy ORM
* PostgreSQL-compatible database configuration through `DATABASE_URL`

---

# System Architecture

```text
┌──────────────────────────────────────┐
│           React Frontend             │
│                                      │
│  Login / Signup                      │
│  User Dashboard                      │
│  Admin Login                         │
│  Admin Dashboard                     │
│  Task Management                     │
│  User Management                     │
└──────────────────┬───────────────────┘
                   │
                   │ HTTP / JSON
                   │ JWT
                   ▼
┌──────────────────────────────────────┐
│            Flask Backend             │
│                                      │
│  Authentication                      │
│  Authorization / RBAC                │
│  Task APIs                           │
│  Admin APIs                          │
│  Validation                          │
│  Business Logic                      │
└──────────────────┬───────────────────┘
                   │
                   │ SQLAlchemy
                   ▼
┌──────────────────────────────────────┐
│             Database                 │
│                                      │
│  Users                               │
│  Tasks                               │
└──────────────────────────────────────┘
```

---

# Project Structure

```text
ToDo_Flask_Backend/
│
├── app.py
├── models.py
├── admin.py
├── requirements.txt
├── .gitignore
├── .env
│
├── API_DOCUMENTATION.md
├── ARCHITECTURE.md
├── README.md
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
└── frontend/
    │
    ├── public/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── context/
    │   ├── pages/
    │   ├── styles/
    │   └── tests/
    │
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    └── index.html
```

---

# Database Design

The application uses two primary models:

```text
User
  │
  │ 1
  │
  │
  │ *
Task
```

## User

The `User` model contains:

```text
id
username
email
password_hash
role
is_active
created_at
```

## Task

The `Task` model contains:

```text
id
user_id
title
description
priority
completed
due_date
created_at
```

## Relationship

One user can have multiple tasks.

The task stores the user's ID through:

```text
Task.user_id
```

This foreign-key relationship is also used for task ownership and authorization.

---

# API Overview

## Authentication

```text
POST /signup
POST /login
POST /admin/login
```

## User Task APIs

```text
POST /tasks
GET /tasks
GET /tasks/<id>
PUT /tasks/<id>
DELETE /tasks/<id>
```

## Admin User APIs

```text
GET /admin/users
PUT /admin/users/<id>
DELETE /admin/users/<id>
```

## Admin Task APIs

```text
GET /admin/tasks
```

For complete request bodies, responses, authentication requirements, validation rules, and error responses, see:

**[API Documentation](API_DOCUMENTATION.md)**

---

# Frontend Architecture

The React frontend is organized into separate responsibilities.

## Pages

The application contains dedicated pages for:

* User login
* User signup
* User dashboard
* Admin login
* Admin dashboard

## Authentication Context

`AuthContext` manages authentication-related state such as:

```text
token
user
isAuthenticated
isAdmin
```

It also provides:

```text
login()
adminLogin()
logout()
```

This allows authentication state to be shared across the application.

## API Layer

The frontend uses a centralized API layer for communication with Flask.

It handles:

* HTTP requests
* JSON request bodies
* JWT Authorization headers
* API responses
* API errors

---

# Routing

The application uses React Router.

## User Routes

```text
/login
/signup
/dashboard
```

Unauthenticated users attempting to access `/dashboard` are redirected to `/login`.

## Admin Routes

```text
/admin/login
/admin/dashboard
```

Unauthenticated users attempting to access `/admin/dashboard` are redirected to `/admin/login`.

Role-based frontend routing also prevents normal users from accessing the admin dashboard.

The backend independently enforces authorization, so frontend routing is not treated as a security boundary.

---

# Testing

The project contains automated tests for both backend and frontend.

## Backend Testing

The Flask backend uses **Pytest**.

Tests cover areas including:

* User registration
* User login
* Authentication errors
* Disabled accounts
* JWT authentication
* Token expiration
* Task CRUD
* Task ownership
* Task filtering
* Admin login
* Admin authorization
* User management
* Role management
* Admin task management

Stable project checkpoint:

```text
55 backend tests passed
```

## Frontend Testing

The React frontend uses:

* Vitest
* React Testing Library
* Jest DOM
* jsdom

Tests cover:

* API functions
* Authentication context
* Authentication persistence
* Protected routes
* Admin routes
* Role-based redirects

Stable project checkpoint:

```text
13 frontend tests passed
```

---

# Input Validation

The backend validates incoming data before modifying the database.

Validation includes:

* Username
* Email
* Password
* Task title
* Task description
* Priority
* Completion status
* Due date
* User role
* Account status

The backend also prevents duplicate usernames and email addresses.

---

# HTTP Status Codes

The API uses standard HTTP status codes to communicate request results.

Examples:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
```

The React frontend uses API responses to display appropriate success and error states.

---

# Environment Configuration

Sensitive configuration is stored using environment variables.

Example:

```text
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

For local development, the application can use SQLite.

The `.env` file is excluded from Git through `.gitignore`.

---

# CORS

The Flask backend is configured to allow communication from the React development server.

Development frontend:

```text
http://localhost:5173
```

This allows the React frontend and Flask API to run independently during development.

---

# Setup

## Prerequisites

Install:

* Python 3.11+
* Node.js
* npm
* Git

---

# Backend Setup

Clone the repository:

```bash
git clone https://github.com/WilhelminaSA/ToDo_Flask_Backend.git
```

Navigate to the project:

```bash
cd ToDo_Flask_Backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
```

Run the Flask backend:

```bash
python app.py
```

The backend runs on:

```text
http://127.0.0.1:5000
```

---

# Frontend Setup

Open a second terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create:

```text
frontend/.env
```

with:

```env
VITE_API_URL=http://127.0.0.1:5000
```

Start the React development server:

```bash
npm run dev
```

The frontend runs on:

```text
http://localhost:5173
```

---

# Running Tests

## Backend

From the project root:

```bash
pytest
```

## Frontend

From the `frontend` directory:

```bash
npm test
```

---

# Documentation

Additional documentation is available in the repository:

### API Documentation

[`API_DOCUMENTATION.md`](API_DOCUMENTATION.md)

Detailed information about:

* Endpoints
* Request methods
* Authentication
* Request bodies
* Responses
* Error handling

### Architecture Documentation

[`ARCHITECTURE.md`](ARCHITECTURE.md)

Detailed information about:

* System architecture
* Frontend architecture
* Backend architecture
* Authentication
* Authorization
* Database design
* Request lifecycle
* Design decisions
* Testing architecture

---

# Future Improvements

Potential future improvements include:

## Authentication

* Email verification
* Password reset
* Refresh tokens
* OAuth/social login
* Multi-factor authentication

## Task Management

* Task categories
* Tags
* Recurring tasks
* Subtasks
* Task attachments
* Reminders
* Advanced search
* Sorting
* Pagination

## Administration

* Audit logs
* Activity monitoring
* Advanced analytics
* Bulk user operations
* Bulk task operations

## Infrastructure

* PostgreSQL production deployment
* Database migrations with Alembic
* Docker
* CI/CD
* Production logging
* Rate limiting
* Production deployment configuration

---

# Screenshots

Screenshots will be added to the repository later.

---

# License

This project is intended as a portfolio and learning project.
