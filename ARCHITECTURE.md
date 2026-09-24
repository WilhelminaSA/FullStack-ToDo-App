# To-Do List Application Architecture

## 1. Overview

The To-Do List application is a full-stack web application consisting of:

* React frontend
* Flask REST API backend
* SQLite database
* JWT-based authentication
* Role-based authorization
* Admin dashboard
* Automated tests

The application follows a **client-server architecture** where the React frontend communicates with the Flask backend through REST API requests.

The backend is responsible for authentication, authorization, validation, business logic, and database operations.

---

## 2. High-Level Architecture

The overall architecture is:

```text
React Frontend
      |
      | HTTP / JSON
      ↓
Flask REST API
      |
      | SQLAlchemy ORM
      ↓
SQLite Database
```

The three main layers are:

1. Presentation layer
2. API and business logic layer
3. Data layer

---

## 3. Presentation Layer

The presentation layer is implemented using React.

The React frontend is responsible for:

* Displaying the user interface
* Login and signup forms
* Task creation and editing
* Task filtering
* Task completion
* Admin dashboard
* User management
* Task management
* Client-side routing
* Managing authentication state
* Sending requests to the Flask API

The frontend does **not** directly communicate with the database.

Instead, it communicates with the Flask backend through REST APIs.

---

## 4. Frontend Architecture

The frontend is organized into several logical areas.

```text
React Application
      |
      +── Pages
      |
      +── Context
      |
      +── API Layer
      |
      +── Styles
      |
      +── Tests
```

### Pages

The application contains pages for:

* User Login
* User Signup
* User Dashboard
* Admin Login
* Admin Dashboard

React Router is used to navigate between these pages.

---

## 5. Authentication Context

Authentication state is managed using **React Context**.

The authentication context keeps track of:

* JWT token
* Current user
* Authentication status
* Admin status
* Login function
* Admin login function
* Logout function

The context allows different components to access authentication information without passing it manually through every component.

For example, components can determine whether the current user is an administrator using the user's role:

```javascript
role === "admin"
```

---

## 6. Frontend API Layer

The frontend contains a centralized API module responsible for communicating with the Flask backend.

The API layer provides functions for operations such as:

```text
signup()
login()
getTasks()
createTask()
updateTask()
deleteTask()
```

Administrative operations include:

```text
adminLogin()
getAdminUsers()
updateAdminUser()
deleteAdminUser()
getAdminTasks()
```

This creates a separation between the UI components and HTTP communication.

Instead of writing `fetch` requests throughout the application, components call reusable API functions.

---

## 7. API Request Flow

A typical frontend request follows this process:

```text
React Component
      ↓
API Function
      ↓
HTTP Request
      ↓
Flask Route
      ↓
Authentication / Authorization
      ↓
Validation
      ↓
Database Operation
      ↓
JSON Response
      ↓
React Component
      ↓
UI Update
```

For protected requests, the JWT is included in the `Authorization` header:

```http
Authorization: Bearer <JWT_TOKEN>
```

---

## 8. Backend Architecture

The backend is implemented using Flask.

The backend is responsible for:

* Defining REST API endpoints
* Validating incoming requests
* Authenticating users
* Verifying JWT tokens
* Checking user roles
* Enforcing task ownership
* Performing CRUD operations
* Managing users
* Managing tasks
* Communicating with the database
* Returning JSON responses

The backend acts as the **main security boundary** of the application.

---

## 9. Backend Structure

The backend is organized into logical modules.

```text
ToDo_Flask_Backend/
|
├── app.py
├── models.py
├── admin.py
├── requirements.txt
├── .env
├── .gitignore
|
├── routes/
│   ├── __init__.py
│   └── auth.py
|
├── utils/
│   ├── __init__.py
│   └── security.py
|
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_tasks.py
    └── test_admin.py
```

---

## 10. `app.py`

`app.py` is the main Flask application entry point.

It is responsible for:

* Creating the Flask application
* Loading environment variables
* Configuring the database
* Configuring CORS
* Initializing SQLAlchemy
* Registering authentication routes
* Defining task routes
* Defining admin routes
* Creating database tables
* Starting the development server

The Flask application uses:

* SQLAlchemy
* Flask-CORS
* python-dotenv
* JWT security utilities

---

## 11. `models.py`

`models.py` contains the database models.

The application has two main entities:

* User
* Task

These are represented using SQLAlchemy models.

The database therefore follows a relational structure.

---

## 12. User Model

The `User` model contains information such as:

* ID
* Username
* Email
* Password hash
* Role
* Active status
* Creation timestamp

Conceptually:

```text
User
|
├── id
├── username
├── email
├── password_hash
├── role
├── is_active
└── created_at
```

The `role` field determines whether the user is:

```text
user
```

or:

```text
admin
```

---

## 13. Task Model

The `Task` model contains information such as:

* Task ID
* User ID
* Title
* Description
* Priority
* Completion status
* Due date
* Creation timestamp

Conceptually:

```text
Task
|
├── id
├── user_id
├── title
├── description
├── priority
├── completed
├── due_date
└── created_at
```

---

## 14. Database Relationship

Each task belongs to one user.

The relationship is:

```text
User 1 ──────────── * Task
```

This means:

* One user can have many tasks.
* Each task belongs to one user.

The `tasks.user_id` column acts as a foreign key referencing the user's ID.

Conceptually:

```text
users.id
    ↑
    |
tasks.user_id
```

This relationship is also important for authorization because the backend can determine which user owns a task.

---

## 15. Why Administrators Are Stored as Users

The application does not maintain a separate administrator table.

Instead, administrators are normal users with an elevated role.

For example:

```text
role = "user"
```

or:

```text
role = "admin"
```

This design was chosen because both normal users and administrators share the same core identity information and authentication mechanism.

The difference is **authorization rather than identity**.

This avoids duplicating user information across separate user and admin tables.

### Interview Explanation

A good way to explain this decision is:

> "I modeled administrators as users with elevated roles instead of creating a separate admin table because both administrators and normal users share the same identity and authentication structure. Authorization determines which operations they are allowed to perform."

---

## 16. Authentication Architecture

The application uses JWT-based authentication.

The authentication process is:

```text
User
  ↓
Login
  ↓
Flask verifies email and password
  ↓
Password hash is checked
  ↓
JWT token is generated
  ↓
Token returned to frontend
  ↓
Frontend stores token
  ↓
Token sent with protected requests
```

The backend does not rely on the frontend to prove authentication.

Every protected request is independently checked by the backend.

---

## 17. Password Security

Passwords are never stored as plain text.

### During Signup

```text
Plain Password
      ↓
Password Hashing
      ↓
Password Hash stored in database
```

### During Login

```text
Password entered by user
      ↓
Password hash verification
      ↓
Authentication succeeds or fails
```

Werkzeug password hashing utilities are used for this process.

This means that even if the database is viewed, the original password is not stored directly.

---

## 18. JWT Authentication Flow

After successful login, the backend creates a JWT.

The frontend stores the token.

For protected requests, the token is sent using:

```http
Authorization: Bearer <JWT_TOKEN>
```

The backend then:

1. Extracts the token.
2. Verifies the token.
3. Identifies the user.
4. Checks whether the account is allowed to perform the operation.
5. Processes the request.

This allows the API to remain stateless with respect to login sessions.

---

## 19. Role-Based Authorization

Authentication answers:

> **"Who are you?"**

Authorization answers:

> **"What are you allowed to do?"**

The application uses the user's role to implement authorization.

There are two roles:

```text
user
admin
```

Normal users can access their own task operations.

Administrators can access administrative operations.

For example:

```text
/tasks
```

is available to authenticated users.

Whereas:

```text
/admin/users
```

requires an administrator.

---

## 20. User Authorization

Normal users are restricted to their own tasks.

For example, suppose:

```text
User A → user_id = 1
User B → user_id = 2
```

If User A requests:

```http
GET /tasks
```

the backend only retrieves tasks where:

```text
user_id = 1
```

User A cannot retrieve User B's tasks by changing a task ID in the frontend.

This authorization is enforced on the backend.

---

## 21. Task Ownership Security

Task ownership is checked for operations such as:

* Get one task
* Update task
* Delete task

The backend verifies:

```text
task.user_id == current_user.id
```

If the task does not belong to the authenticated user, the backend does not allow the operation.

This prevents **horizontal privilege escalation**, where one user attempts to access another user's resources.

---

## 22. Admin Authorization Flow

An administrator must first authenticate through:

```http
POST /admin/login
```

The backend verifies:

* User exists.
* Password is correct.
* Account is active.
* User has `role = admin`.

After successful authentication, the backend returns a JWT.

When the administrator accesses an admin endpoint:

```text
/admin/users
/admin/tasks
```

the backend verifies the JWT and then checks the user's role.

Only an administrator is allowed to continue.

---

## 23. Security Utility Layer

Reusable authentication and authorization logic is kept inside:

```text
utils/security.py
```

This module contains reusable security functionality such as:

* JWT generation
* Token validation
* Authentication decorators
* Admin authorization
* Email validation

Keeping this logic in one place avoids duplicating authentication code across routes.

---

## 24. Authentication Routes

Authentication-related routes are separated into:

```text
routes/auth.py
```

This module handles:

```text
POST /signup
POST /login
```

This provides separation between authentication logic and the main task/admin API functionality.

---

## 25. Admin Routes

Administrative operations include:

```text
POST /admin/login
GET /admin/users
PUT /admin/users/<id>
DELETE /admin/users/<id>
GET /admin/tasks
```

These operations require administrator authorization except for the admin login endpoint.

The current implementation keeps the admin route handlers in `app.py`.

The `admin.py` module exists as a blueprint module, but the active admin routes are currently defined directly in `app.py`.

---

## 26. Separation of Concerns

The application separates responsibilities across different layers.

### Frontend

Responsible for:

* UI
* User interaction
* Client-side routing
* Authentication state
* Displaying API responses

### API Layer

Responsible for:

* HTTP communication
* Sending authentication tokens
* Handling API responses and errors

### Flask Backend

Responsible for:

* Authentication
* Authorization
* Validation
* Business logic
* API endpoints

### Security Utilities

Responsible for:

* JWT handling
* Authentication decorators
* Admin authorization
* Validation utilities

### Models

Responsible for:

* Database representation
* User data
* Task data
* Relationships

### Database

Responsible for:

* Persistent storage of users
* Persistent storage of tasks

---

## 27. Request Lifecycle

A protected task request can be understood as follows:

```text
React Dashboard
      ↓
createTask() / updateTask() / deleteTask()
      ↓
API request
      ↓
Authorization header
      ↓
Flask route
      ↓
JWT validation
      ↓
Current user identified
      ↓
Request validation
      ↓
Task ownership check
      ↓
SQLAlchemy database operation
      ↓
JSON response
      ↓
React updates the UI
```

This layered flow keeps security and database operations on the server side.

---

## 28. Error Handling

The backend validates incoming requests before performing database operations.

Examples of invalid requests include:

* Missing required fields
* Invalid email
* Short password
* Invalid priority
* Invalid role
* Invalid date
* Invalid boolean value
* Duplicate username
* Duplicate email
* Non-existent task
* Unauthorized task access

The API returns appropriate HTTP status codes such as:

* `400 Bad Request`
* `401 Unauthorized`
* `403 Forbidden`
* `404 Not Found`
* `409 Conflict`

---

## 29. CORS Architecture

The React frontend and Flask backend run on different development servers.

For example:

```text
React
http://localhost:5173
```

and:

```text
Flask
http://127.0.0.1:5000
```

Because these are different origins, **Cross-Origin Resource Sharing (CORS)** is configured in Flask.

The backend currently allows the frontend development origin:

```text
http://localhost:5173
```

This allows the browser to make API requests from the React application to Flask.

---

## 30. Environment Configuration

Sensitive configuration is stored using environment variables.

The backend uses a `.env` file for values such as:

```text
SECRET_KEY
```

The application loads these values using `python-dotenv`.

The `.env` file is excluded from Git using `.gitignore`.

This prevents sensitive configuration from being committed to the repository.

---

## 31. Database Architecture

The application currently uses SQLite for local development.

The database contains two main tables:

```text
users
tasks
```

Conceptually:

```text
users
+----------------+
| id             |
| username       |
| email          |
| password_hash  |
| role           |
| is_active      |
| created_at     |
+----------------+
        |
        | 1
        |
        | many
        ↓
tasks
+----------------+
| id             |
| user_id        |
| title          |
| description    |
| priority       |
| completed      |
| due_date       |
| created_at     |
+----------------+
```

SQLAlchemy is used as the ORM.

This means application code interacts with Python model objects instead of writing raw SQL for every database operation.

---

## 32. Why SQLAlchemy ORM Is Used

SQLAlchemy provides an abstraction over database operations.

For example, instead of manually writing SQL for every operation, the application can work with:

```text
User
Task
```

model objects.

Advantages include:

* Cleaner Python code
* Object-oriented database interaction
* Easier relationship management
* Reduced repetitive SQL
* Easier database portability

---

## 33. Frontend Routing Architecture

React Router controls navigation between application pages.

Main routes include:

```text
/
/login
/signup
/dashboard
/admin/login
/admin/dashboard
```

The root route redirects to the dashboard.

Protected routes check authentication before rendering the page.

---

## 34. Protected User Route

The user dashboard is protected.

The logic is conceptually:

```text
Is the user authenticated?
      |
     No
      ↓
Redirect to /login

      Yes
      ↓
Is the user an admin?
      |
     Yes
      ↓
Redirect to /admin/dashboard

      No
      ↓
Show user dashboard
```

This prevents normal unauthenticated users from accessing the dashboard.

---

## 35. Protected Admin Route

The admin dashboard has a separate protection layer.

The logic is:

```text
Is the user authenticated?
      |
     No
      ↓
Redirect to /admin/login

      Yes
      ↓
Is role = admin?
      |
     No
      ↓
Redirect to /dashboard

      Yes
      ↓
Show admin dashboard
```

This provides frontend navigation protection.

However, the backend still performs the actual authorization checks.

---

## 36. Why Backend Authorization Is Still Required

Frontend route protection improves the user experience, but it is **not a security boundary**.

A user could bypass the React application and directly send an HTTP request to the backend.

Therefore, the backend must independently verify:

* JWT validity
* User identity
* User role
* Resource ownership

This follows the principle:

> **Never trust the client for authorization.**

The frontend controls navigation.

The backend controls access.

---

## 37. Admin Dashboard Architecture

The admin dashboard communicates with two main API areas:

```text
/admin/users
```

and:

```text
/admin/tasks
```

The dashboard can display information such as:

* Total users
* Active users
* Number of administrators
* Total tasks
* Completed tasks

The administrator can also:

* Search users
* Activate users
* Deactivate users
* Change roles
* Delete users
* Search tasks
* Filter tasks
* Delete tasks

---

## 38. Testing Architecture

The project contains automated tests for both backend and frontend functionality.

### Backend Testing

The backend uses **pytest**.

The tests are organized into:

```text
test_auth.py
test_tasks.py
test_admin.py
```

A shared test configuration is provided through:

```text
conftest.py
```

Current backend test result:

```text
55 / 55 tests passed
```

### Frontend Testing

The frontend uses:

* Vitest
* React Testing Library
* jsdom

Frontend tests cover areas such as:

* API functions
* Authentication context
* Application routing
* Protected routes
* Admin route behavior

Current frontend test result:

```text
13 / 13 tests passed
```

---

## 39. Development Environment

The application runs as two separate development processes.

### Backend

```text
Flask
http://127.0.0.1:5000
```

### Frontend

```text
React + Vite
http://localhost:5173
```

The frontend communicates with the backend through HTTP requests.

The database runs locally through SQLite.

---

## 40. Complete System Flow

The complete application can be visualized as:

```text
User
  |
  ↓
React UI
  |
  ↓
React Router
  |
  ↓
Authentication Context
  |
  ↓
API Layer
  |
  | HTTP + JWT
  ↓
Flask REST API
  |
  +-------------------+
  |                   |
  ↓                   ↓
Security          Route Logic
  |                   |
  |                   ↓
  |              Validation
  |                   |
  +--------→ SQLAlchemy
                      |
                      ↓
                 SQLite Database
```

The response then travels back through the same application layers to update the React UI.

---

## 41. Important Design Decisions

### 1. JWT Authentication

JWT was selected to authenticate API requests without maintaining traditional server-side login sessions.

### 2. Role-Based Authorization

Administrators and normal users share the same user model, while the role determines access permissions.

### 3. Task Ownership

Each task stores a `user_id`, allowing the backend to enforce ownership.

### 4. SQLAlchemy

SQLAlchemy provides an ORM-based approach to database operations.

### 5. Server-Side Validation

The backend validates incoming data even when the frontend performs validation.

### 6. Environment Variables

Sensitive configuration is kept outside the source code.

### 7. Centralized Security Utilities

JWT and authorization logic are reused through security utility functions and decorators.

### 8. Centralized Frontend API Layer

API requests are kept in one module instead of being duplicated throughout React components.

---

## 42. Current Architecture Limitations

The current architecture is designed primarily for local development and a placement/project demonstration.

Current limitations include:

* SQLite is being used as the development database.
* Flask is running with the development server.
* Frontend and backend are running separately.
* CORS is configured for the local frontend origin.
* No production deployment infrastructure is currently configured.
* No production-grade monitoring or logging system is currently implemented.

These are development-stage decisions rather than requirements of the application's core architecture.

---

## 43. Possible Future Improvements

If the application were moved toward production, possible improvements could include:

* PostgreSQL as the production database
* Production WSGI server such as Gunicorn
* HTTPS
* Secure cookie or token-storage strategy depending on deployment requirements
* Rate limiting
* Centralized logging
* Monitoring
* Automated CI/CD
* Containerization using Docker
* Cloud deployment
* Database migrations
* Pagination for large datasets
* More granular permissions
* Refresh-token based authentication

These are future improvements and are not currently part of the implemented local architecture.

---

## 44. Interview Explanation

A concise interview explanation of the architecture is:

> "I built the application using a client-server architecture. The frontend is developed with React and communicates with a Flask REST API using JSON over HTTP. Flask handles authentication, authorization, validation, and business logic, while SQLAlchemy is used as the ORM for SQLite. Authentication is implemented using JWTs, and role-based authorization separates normal users from administrators. Each task is associated with a user through a foreign key, which allows the backend to enforce task ownership. The frontend also has protected routes for user and admin dashboards, while the backend independently enforces the actual security rules."

---

## 45. Architecture in One Diagram

```text
+------------------------------------------------------+
|                    React Frontend                    |
|                                                      |
|  Login | Signup | Dashboard | Admin Dashboard       |
|                 |                                    |
|          AuthContext + Router                        |
|                 |                                    |
|              API Layer                               |
+------------------|-----------------------------------+
                   |
                   | HTTP / JSON
                   | Authorization: Bearer JWT
                   ↓
+------------------------------------------------------+
|                     Flask API                        |
|                                                      |
|  Authentication                                      |
|  Authorization                                       |
|  Validation                                          |
|  Task CRUD                                           |
|  Admin Management                                    |
|                                                      |
|       Security Utilities + Routes                    |
+------------------|-----------------------------------+
                   |
                   | SQLAlchemy
                   ↓
+------------------------------------------------------+
|                    SQLite DB                         |
|                                                      |
|                 users                                |
|                    |                                 |
|                    | 1:N                             |
|                    ↓                                 |
|                  tasks                               |
+------------------------------------------------------+
```

---

## 46. Final Architecture Summary

The application follows a layered full-stack architecture:

```text
React
  ↓
REST API
  ↓
Flask
  ↓
Security + Business Logic
  ↓
SQLAlchemy
  ↓
SQLite
```

The most important architectural principles are:

* Separation of frontend and backend
* RESTful API communication
* JWT-based authentication
* Role-based authorization
* Server-side validation
* Task ownership enforcement
* ORM-based database interaction
* Centralized security utilities
* Centralized frontend API communication
* Automated testing

The frontend provides the user experience, while the backend remains responsible for enforcing authentication, authorization, validation, and data access rules.
