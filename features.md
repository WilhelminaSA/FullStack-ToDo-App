# Features

## 1. Project Overview

This project is a full-stack To-Do application built with:

* React for the frontend
* Flask for the backend REST API
* SQLAlchemy for database interaction
* SQLite for local development
* JWT for authentication
* Role-Based Access Control (RBAC) for user and admin authorization
* Pytest for backend testing
* Vitest and React Testing Library for frontend testing

The application provides separate experiences for normal users and administrators.

---

# 2. User Features

## 2.1 User Registration

Users can create an account using:

* Username
* Email
* Password

### Validation

The backend validates:

* Required fields
* Username format and length
* Email format
* Password requirements
* Duplicate username
* Duplicate email

Passwords are never stored as plain text. They are stored as securely generated password hashes.

---

## 2.2 User Login

Registered users can log in using:

* Email
* Password

After successful authentication, the backend generates a JWT access token.

The frontend stores the authentication information locally and uses the token for protected API requests.

---

## 2.3 Persistent Login

The frontend stores the authentication token and user information in browser `localStorage`.

This allows the user to remain logged in after:

* Page refresh
* Browser navigation
* Restarting the Flask development server

The user can explicitly log out to remove the stored authentication information.

---

## 2.4 User Dashboard

Authenticated users have access to a dedicated dashboard.

The dashboard provides:

* Task list
* Task creation
* Task editing
* Task deletion
* Task completion
* Task filtering
* Task statistics
* Loading states
* Error states
* Empty states

The dashboard communicates with the Flask REST API rather than maintaining tasks only in frontend memory.

---

# 3. Task Management

## 3.1 Create Tasks

Users can create tasks containing:

* Title
* Description
* Priority
* Due date

The task is automatically associated with the authenticated user.

The frontend does not decide which user owns the task. The backend obtains the user identity from the JWT token.

---

## 3.2 Task Titles

Task titles are required.

The backend validates that:

* A title is provided
* The title is a string
* The title is not empty
* The title does not exceed the allowed length

Maximum title length:

```text
100 characters
```

---

## 3.3 Task Descriptions

Users can optionally add a description to a task.

Descriptions can be updated later.

A task can also have no description.

---

## 3.4 Task Priorities

Every task has a priority.

Supported priorities:

* Low
* Medium
* High

If the user does not provide a priority while creating a task, the default priority is:

```text
Medium
```

The frontend displays different visual styles for different priority levels.

---

## 3.5 Due Dates

Users can optionally assign a due date to a task.

The backend expects dates in:

```text
YYYY-MM-DD
```

Example:

```text
2026-09-30
```

Due dates can also be removed when updating a task.

---

## 3.6 Complete and Uncomplete Tasks

Users can mark tasks as:

```text
completed = true
```

or:

```text
completed = false
```

The frontend provides an easy way to change the completion status.

---

## 3.7 Edit Tasks

Users can update their own tasks.

The following fields can be updated:

* Title
* Description
* Priority
* Completion status
* Due date

The backend validates the updated values before saving them.

---

## 3.8 Delete Tasks

Users can permanently delete their own tasks.

A user cannot delete another user's task.

The backend verifies task ownership before performing the deletion.

---

# 4. Task Filtering

The user dashboard supports filtering tasks.

## 4.1 Completion Filter

Users can filter tasks based on whether they are:

* All
* Completed
* Pending

---

## 4.2 Priority Filter

Users can filter tasks by:

* All
* Low
* Medium
* High

---

## 4.3 Combined Filtering

The frontend can apply multiple filters together.

For example:

```text
Pending + High Priority
```

This allows users to quickly find important unfinished tasks.

---

# 5. Dashboard Statistics

The user dashboard displays task-related statistics.

Examples include:

* Total tasks
* Completed tasks
* Pending tasks
* Other task summaries supported by the dashboard

These statistics are calculated from the user's tasks.

---

# 6. Admin Features

The application provides a separate administration interface.

Administrators are authenticated users with:

```text
role = admin
```

There is no separate Admin table.

This means an administrator still uses the same underlying `User` model but receives additional permissions through their role.

---

# 7. Admin Login

Administrators have a dedicated login page.

Admin authentication verifies:

1. Email
2. Password
3. User existence
4. Account status
5. Admin role

Only users with the administrator role can successfully access the admin dashboard.

---

# 8. Admin Dashboard

Administrators have access to a dedicated dashboard.

The dashboard provides an overview of:

* Total users
* Active users
* Number of administrators
* Total tasks
* Completed tasks

The admin dashboard also provides separate interfaces for managing users and tasks.

---

# 9. Admin User Management

Administrators can view registered users.

User information includes:

* User ID
* Username
* Email
* Role
* Account status
* Account creation date

---

## 9.1 Search Users

Administrators can search users using the available user-management interface.

This helps locate specific accounts without manually scanning the complete user list.

---

## 9.2 Activate and Deactivate Users

Administrators can change a user's account status.

A user can be:

```text
Active
```

or:

```text
Inactive
```

Disabled users cannot log in normally.

This provides administrators with control over account access without immediately deleting the account.

---

## 9.3 Change User Roles

Administrators can change a user's role between:

```text
user
```

and:

```text
admin
```

This allows the application to support multiple levels of access using role-based authorization.

---

## 9.4 Update User Information

Administrators can update supported user information such as:

* Username
* Email
* Role
* Account status

The backend validates the updated values and prevents duplicate usernames or emails.

---

## 9.5 Delete Users

Administrators can delete user accounts.

However, an administrator cannot delete their own currently authenticated account.

This prevents an administrator from accidentally removing the account being used to perform the operation.

---

# 10. Admin Task Management

Administrators can view tasks across the application.

Unlike normal users, administrators are not restricted to tasks belonging to their own account.

The admin task interface provides access to:

* Task information
* Task owner
* Priority
* Completion status
* Due date
* Creation date

Administrators can also delete tasks when required.

---

# 11. Role-Based Access Control

The application uses Role-Based Access Control (RBAC).

There are two primary roles:

```text
user
admin
```

## User permissions

A normal user can:

* Manage their own account through authentication
* Create tasks
* View their own tasks
* Update their own tasks
* Delete their own tasks

## Admin permissions

An administrator can:

* Access the admin dashboard
* View users
* Update users
* Activate/deactivate users
* Change user roles
* Delete users
* View all tasks
* Delete tasks

Authorization is enforced by the backend, not only by the frontend.

---

# 12. Task Ownership and Data Isolation

Every task contains a `user_id`.

This identifies the user who owns the task.

For normal users, protected task operations verify that:

```text
task.user_id == authenticated_user.id
```

Therefore, a user cannot access or modify another user's task simply by changing the task ID in an API request.

This is an important backend authorization rule.

---

# 13. JWT Authentication

The application uses JSON Web Tokens (JWT) for authentication.

After successful login, the server generates a token containing relevant authentication information.

The frontend sends the token using the HTTP Authorization header:

```text
Authorization: Bearer <token>
```

Protected backend routes validate the token before allowing access.

---

# 14. Token-Based Authorization

Protected endpoints require a valid authentication token.

The backend checks:

* Whether the Authorization header exists
* Whether the Bearer token format is valid
* Whether the token is valid
* Whether the token has expired
* The identity associated with the token
* The user's role when required

Invalid or missing authentication results in an appropriate HTTP error response.

---

# 15. Password Security

Passwords are not stored directly in the database.

Instead, password hashing is used.

The general authentication flow is:

```text
User password
      ↓
Password hashing
      ↓
Password hash stored in database
```

During login:

```text
Entered password
      ↓
Compare with stored password hash
      ↓
Authentication result
```

This prevents the database from storing users' original passwords.

---

# 16. Backend REST API

The Flask backend provides REST-style API endpoints for the application.

### Authentication

```text
POST /signup
POST /login
POST /admin/login
```

### User task management

```text
POST /tasks
GET /tasks
GET /tasks/<id>
PUT /tasks/<id>
DELETE /tasks/<id>
```

### Admin user management

```text
GET /admin/users
PUT /admin/users/<id>
DELETE /admin/users/<id>
```

### Admin task management

```text
GET /admin/tasks
```

---

# 17. Frontend API Layer

The React frontend uses a centralized API layer.

The API layer handles:

* API requests
* HTTP methods
* JSON request bodies
* Authorization headers
* JWT token attachment
* API response handling
* Error handling

This prevents API request logic from being duplicated throughout the frontend.

The main API functions include:

```text
signup()
login()
getTasks()
createTask()
updateTask()
deleteTask()

adminLogin()
getAdminUsers()
updateAdminUser()
deleteAdminUser()
getAdminTasks()
```

---

# 18. React Authentication Context

The frontend uses React Context to manage authentication state.

The authentication context provides information such as:

```text
token
user
isAuthenticated
isAdmin
```

It also provides authentication operations such as:

```text
login()
adminLogin()
logout()
```

This allows different components to access authentication information without manually passing it through multiple component levels.

---

# 19. Protected Frontend Routes

The frontend uses protected routes for authorization-aware navigation.

## User protected route

Unauthenticated users attempting to access:

```text
/dashboard
```

are redirected to:

```text
/login
```

---

## Admin protected route

Unauthenticated users attempting to access:

```text
/admin/dashboard
```

are redirected to:

```text
/admin/login
```

---

## Role-based frontend routing

A normal user attempting to access the admin dashboard is redirected to the user dashboard.

An administrator attempting to access the normal user dashboard is redirected to the admin dashboard.

These frontend checks improve the user experience, while the backend remains responsible for actual authorization enforcement.

---

# 20. Loading, Error, and Empty States

The React frontend handles common asynchronous states.

## Loading state

Displayed while data is being retrieved from the backend.

## Error state

Displayed when an API request fails.

## Empty state

Displayed when there are no tasks or no matching results.

These states make the application easier to understand and use.

---

# 21. Database

The backend uses SQLAlchemy as its ORM.

The primary database models are:

```text
User
Task
```

---

## User Model

The `User` model contains fields such as:

```text
id
username
email
password_hash
role
is_active
created_at
```

---

## Task Model

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

---

# 22. User-Task Relationship

The relationship between users and tasks is:

```text
One User
   │
   ├── Task 1
   ├── Task 2
   ├── Task 3
   └── ...
```

One user can have many tasks.

Each task belongs to one user through:

```text
Task.user_id
```

This relationship is also used for enforcing task ownership.

---

# 23. Database Configuration

The application supports configuration through environment variables.

The database connection can be configured using:

```text
DATABASE_URL
```

For local development, SQLite is used by default.

The local database is stored inside the application's instance directory.

The database file is excluded from Git using `.gitignore`.

---

# 24. CORS Support

The Flask backend is configured to allow requests from the React development server.

The current frontend development origin is:

```text
http://localhost:5173
```

This allows the React frontend and Flask backend to communicate while running on different development ports.

---

# 25. Input Validation

The backend validates incoming API data before modifying the database.

Validation is applied to fields such as:

* Username
* Email
* Password
* Title
* Description
* Priority
* Completion status
* Due date
* User role
* Account status

Invalid input produces an appropriate error response rather than being blindly stored.

---

# 26. Duplicate Data Protection

The backend prevents duplicate values for fields that must be unique.

Examples include:

* Username
* Email

The database also defines uniqueness constraints where appropriate.

This provides an additional layer of protection beyond frontend validation.

---

# 27. Error Handling

The API returns HTTP status codes that communicate the result of a request.

Examples include:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
```

This allows the React frontend to determine whether an operation succeeded or failed and display an appropriate message.

---

# 28. Frontend Styling

The React application includes dedicated styling for:

* Authentication pages
* User dashboard
* Tasks
* Filters
* Priority indicators
* Admin dashboard
* User management
* Task management
* Buttons
* Forms
* Error messages
* Empty states
* Responsive layouts

The admin interface uses separate styling to distinguish administrative functionality from the normal user experience.

---

# 29. Responsive User Interface

The frontend is designed to remain usable across different screen sizes.

The interface uses responsive CSS so that the dashboard, forms, task cards, and administrative sections can adapt to different viewport sizes.

---

# 30. Automated Backend Testing

The Flask backend includes automated tests using Pytest.

The tests cover areas including:

* Home endpoint
* User registration
* User login
* Invalid authentication
* Disabled accounts
* JWT authentication
* Token expiration
* Task creation
* Task retrieval
* Task updates
* Task deletion
* Task ownership
* Task filtering
* Admin login
* Admin authorization
* User management
* Role management
* Admin task management
* Self-deletion protection

The backend test suite reached:

```text
55 passed
```

at the stable project checkpoint.

---

# 31. Automated Frontend Testing

The React frontend includes automated tests using:

* Vitest
* React Testing Library
* Jest DOM matchers
* jsdom

The tests cover:

* API functions
* Authentication context
* Login state
* Authentication persistence
* User routing
* Admin routing
* Protected routes
* Role-based redirects

The current frontend test suite contains:

```text
13 tests
```

with the stable checkpoint showing:

```text
13 passed
```

---

# 32. Full-Stack Architecture

The application follows a client-server architecture.

```text
┌──────────────────────────────┐
│        React Frontend        │
│                              │
│  Login / Signup              │
│  User Dashboard              │
│  Admin Dashboard             │
│  Task Management             │
└──────────────┬───────────────┘
               │
               │ HTTP / JSON
               │ JWT
               ▼
┌──────────────────────────────┐
│        Flask Backend         │
│                              │
│  Authentication              │
│  Authorization / RBAC        │
│  Task APIs                   │
│  Admin APIs                  │
│  Validation                  │
└──────────────┬───────────────┘
               │
               │ SQLAlchemy
               ▼
┌──────────────────────────────┐
│          Database            │
│                              │
│  Users                       │
│  Tasks                       │
└──────────────────────────────┘
```

---

# 33. Separation of Responsibilities

The project separates responsibilities between the frontend and backend.

## Frontend

Responsible for:

* User interface
* Navigation
* Form interaction
* Displaying data
* Client-side state
* API communication
* User experience

## Backend

Responsible for:

* Authentication
* Authorization
* Business rules
* Input validation
* Task ownership
* Database operations
* Security-sensitive decisions
* API responses

## Database

Responsible for:

* Persistent storage
* User records
* Task records
* Relationships
* Data constraints

---

# 34. Security Design

The project includes several security-related measures:

* Password hashing
* JWT authentication
* Protected API routes
* Role-based authorization
* Task ownership checks
* Disabled-account checks
* Admin authorization
* Self-deletion protection
* Environment-based secret configuration
* `.env` excluded from Git
* Database excluded from Git
* Backend-side input validation

Security decisions are enforced on the backend rather than relying solely on frontend restrictions.

---

# 35. Project Documentation

The repository includes separate documentation for different aspects of the project.

### README

Provides:

* Project overview
* Features
* Technology stack
* Setup instructions
* Project structure
* API overview
* Testing information

### API Documentation

`API_DOCUMENTATION.md`

Contains:

* API endpoints
* Request methods
* Authentication requirements
* Request bodies
* Response formats
* Error responses

### Architecture Documentation

`ARCHITECTURE.md`

Contains:

* System architecture
* Frontend architecture
* Backend architecture
* Authentication flow
* Authorization flow
* Database design
* Request lifecycle
* Design decisions
* Testing architecture

### Features Documentation

`features.md`

Contains the complete functional feature set of the application.

---

# 36. Development Features

The project is structured to support continued development.

The codebase separates major responsibilities into areas such as:

```text
Frontend
├── Components
├── Pages
├── Context
├── API
├── Styles
└── Tests

Backend
├── Routes
├── Models
├── Utilities
├── Tests
└── Configuration
```

This structure makes individual parts easier to modify and test.

---

# 37. Current Limitations

The current application is primarily designed as a portfolio and learning project.

Some production-level features are not currently implemented, such as:

* Password reset
* Email verification
* Refresh-token rotation
* Production deployment configuration
* Database migrations
* Rate limiting
* Advanced audit logging
* Advanced task pagination
* Real-time task updates
* Cloud file storage
* Automated CI/CD deployment pipeline

These can be added as future improvements.

---

# 38. Potential Future Improvements

Possible future enhancements include:

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
* Task reminders
* Sorting
* Pagination
* Advanced search

## Admin

* Audit logs
* Activity monitoring
* More detailed analytics
* Bulk user operations
* Bulk task operations

## Infrastructure

* PostgreSQL production deployment
* Database migrations with Alembic
* Docker
* CI/CD
* Automated deployment
* Production logging
* Rate limiting

---

# 39. Key Technical Concepts Demonstrated

This project demonstrates practical understanding of:

* React
* React Router
* React Context
* React state management
* REST APIs
* Flask
* SQLAlchemy
* Relational databases
* JWT authentication
* Password hashing
* Role-Based Access Control
* Authorization
* CRUD operations
* HTTP methods
* HTTP status codes
* JSON APIs
* CORS
* Environment variables
* Input validation
* Database relationships
* Automated testing
* API integration
* Client-server architecture
* Protected routes
* Error handling

---

# 40. Placement/Interview Relevance

This project can be discussed in interviews as an example of building a complete application rather than only an isolated frontend or backend.

Important concepts demonstrated include:

### Authentication

How users securely log in and receive JWT tokens.

### Authorization

How the backend determines whether a user is allowed to perform a particular operation.

### RBAC

How the same user model supports different permissions through the `role` field.

### CRUD

How users create, read, update, and delete tasks through REST APIs.

### Database Design

How users and tasks are connected using a foreign-key relationship.

### Security

How password hashing, JWT validation, role checks, and task ownership protect application resources.

### Frontend-Backend Integration

How a React frontend communicates with a Flask backend using HTTP and JSON.

### Testing

How automated tests verify backend API behavior and frontend routing/authentication behavior.

---

# 41. Feature Summary

| Area                 | Features                                            |
| -------------------- | --------------------------------------------------- |
| Authentication       | Signup, login, logout, JWT                          |
| User Management      | User account, persistent authentication             |
| Tasks                | Create, view, update, delete                        |
| Task Status          | Complete/uncomplete                                 |
| Priority             | Low, Medium, High                                   |
| Due Dates            | Add, update, remove                                 |
| Filtering            | Completion and priority filters                     |
| User Dashboard       | Tasks, statistics, loading/error/empty states       |
| Admin Authentication | Dedicated admin login                               |
| Admin Users          | View, search, update, activate/deactivate, delete   |
| Admin Roles          | Promote/demote users                                |
| Admin Tasks          | View and manage application-wide tasks              |
| Authorization        | JWT + RBAC + ownership checks                       |
| Database             | SQLAlchemy + SQLite development database            |
| Frontend             | React + React Router                                |
| Backend              | Flask REST API                                      |
| Security             | Password hashing, JWT, validation, protected routes |
| Testing              | Pytest + Vitest + React Testing Library             |
| Documentation        | README, API docs, architecture docs, feature docs   |

---

# 42. Overall Application Flow

```text
User
 │
 ├── Sign Up
 │      ↓
 │   User Account
 │
 ├── Login
 │      ↓
 │   JWT Token
 │      ↓
 │   User Dashboard
 │      ↓
 │   Create / View / Update / Delete Tasks
 │
 └───────────────────────────────┐
                                 │
Administrator                     │
 │                               │
 ├── Admin Login                 │
 │      ↓                        │
 │   JWT Token                   │
 │      ↓                        │
 │   Admin Dashboard             │
 │      ↓                        │
 │   ├── Manage Users            │
 │   └── Manage Tasks             │
 │                               │
 └───────────────────────────────┘

             ↓
       Flask REST API
             ↓
        SQLAlchemy ORM
             ↓
          Database
```

---

# 43. Final Summary

The application provides a complete full-stack To-Do management system with:

* React frontend
* Flask REST API
* User authentication
* JWT-based authorization
* Role-Based Access Control
* User task management
* Task filtering
* Task priorities
* Due dates
* Admin authentication
* Admin user management
* Admin task management
* Task ownership protection
* Password hashing
* Input validation
* CORS configuration
* Persistent database storage
* Automated backend testing
* Automated frontend testing
* Separate API and architecture documentation

The project demonstrates how a modern web application can connect a React client, Flask API, authentication/authorization layer, and relational database into a single full-stack system.
