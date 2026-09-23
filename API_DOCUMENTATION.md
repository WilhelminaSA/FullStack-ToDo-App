To-Do List API Documentation
1. Overview

This document describes the REST API for the To-Do List application.

The backend is built using Flask and provides:

User registration
User login
JWT-based authentication
Task CRUD operations
Task filtering
Admin authentication
Admin user management
Admin task management
Role-based authorization
2. Technology Stack
Technology	Purpose
Python	Backend programming language
Flask	Web framework
Flask-SQLAlchemy	ORM and database interaction
SQLite	Development database
PyJWT	JWT authentication
Werkzeug	Password hashing
Flask-CORS	Frontend-backend communication
python-dotenv	Environment variable management
pytest	Backend automated testing
3. Base URL

During local development, the Flask backend runs at:

http://127.0.0.1:5000

The React frontend runs separately using Vite.

The default Vite development URL is:

http://localhost:5173

If port 5173 is already in use, Vite automatically uses another available port, such as:

http://localhost:5174
4. Authentication

The application uses JSON Web Tokens (JWT) for authentication.

After successful login, the backend returns a JWT token.

The frontend stores the token and sends it with protected requests using the HTTP Authorization header:

Authorization: Bearer <JWT_TOKEN>

Protected endpoints verify the token before allowing access.

5. User Roles

The application has two roles:

user
admin
User

A normal user can:

Create their own tasks
View their own tasks
Update their own tasks
Delete their own tasks
Filter their own tasks
Admin

An administrator can:

Access the admin dashboard
View users
Update users
Activate or deactivate users
Change user roles
Delete users
View all tasks
Delete tasks

Administrators are stored in the same users table as normal users.

The difference is determined by the role field.

For example:

role = user

or:

role = admin
6. Common Response Format

Successful responses generally return JSON.

Example:

{
  "message": "Task created successfully",
  "task_id": 1
}

Error responses generally use:

{
  "error": "Error message"
}

Some validation errors use:

{
  "message": "Error message"
}
7. API Endpoint Summary
Method	Endpoint	Authentication	Purpose
GET	/	None	API welcome message
POST	/signup	None	Register user
POST	/login	None	User login
POST	/tasks	User	Create task
GET	/tasks	User	Get user's tasks
GET	/tasks/<id>	User	Get one task
PUT	/tasks/<id>	User	Update task
DELETE	/tasks/<id>	User	Delete task
POST	/admin/login	None	Admin login
GET	/admin/users	Admin	Get all users
PUT	/admin/users/<id>	Admin	Update user
DELETE	/admin/users/<id>	Admin	Delete user
GET	/admin/tasks	Admin	Get all tasks
8. Welcome Endpoint
GET /

Returns a welcome message from the API.

Authentication

None.

Response

Status: 200 OK

{
  "message": "Welcome to the To-Do List API"
}
9. User Registration
POST /signup

Creates a new user account.

Authentication

None.

Request Body
{
  "username": "Sneha",
  "email": "sneha@example.com",
  "password": "password123"
}
Validation
Username must be a string.
Username must contain 3–50 characters.
Email must have a valid email format.
Password must contain at least 8 characters.
Username must be unique.
Email must be unique.
Default User Values

New users are automatically created with:

role = user
is_active = true

Users cannot create an admin account through /signup.

Success Response

Status: 201 Created

{
  "message": "User registered successfully"
}
10. User Login
POST /login

Authenticates a normal user and returns a JWT token.

Authentication

None.

Request Body
{
  "email": "sneha@example.com",
  "password": "password123"
}
Validation
Email is required.
Password is required.
Email must have a valid email format.
Password must contain at least 8 characters.
Success Response

Status: 200 OK

Example:

{
  "message": "Login successful",
  "access_token": "<JWT_TOKEN>",
  "user_id": 1,
  "username": "Sneha",
  "email": "sneha@example.com",
  "role": "user"
}

The frontend uses the returned token for protected API requests.

11. Create Task
POST /tasks

Creates a task for the currently authenticated user.

Authentication

Required.

Authorization: Bearer <JWT_TOKEN>
Request Body
{
  "title": "Complete DBMS revision",
  "description": "Revise joins and window functions",
  "priority": "High",
  "due_date": "2026-09-25"
}
Fields
Field	Required	Description
title	Yes	Task title
description	No	Task description
priority	No	Low, Medium, or High
due_date	No	Date in YYYY-MM-DD format

If priority is omitted, the backend uses:

Medium

The user_id is obtained from the authenticated JWT rather than being supplied by the client.

A newly created task has:

completed = false
Success Response

Status: 201 Created

{
  "message": "Task created successfully",
  "task_id": 1,
  "title": "Complete DBMS revision",
  "description": "Revise joins and window functions",
  "priority": "High",
  "completed": false,
  "due_date": "2026-09-25",
  "created_at": "2026-09-21T..."
}
12. Get User Tasks
GET /tasks

Returns tasks belonging to the currently authenticated user.

Authentication

Required.

Basic Request
GET /tasks
Optional Filters

The endpoint supports filtering by completion status and priority.

Filter by Completion
GET /tasks?completed=true

or:

GET /tasks?completed=false
Filter by Priority
GET /tasks?priority=High

Supported priority values:

Low
Medium
High
Multiple Filters

Filters can be combined.

Example:

GET /tasks?completed=false&priority=High
Important Security Rule

A normal user can only retrieve their own tasks.

The backend uses the authenticated user's ID when querying tasks.

Success Response

Status: 200 OK

[
  {
    "id": 1,
    "user_id": 2,
    "title": "Complete DBMS revision",
    "description": "Revise joins",
    "priority": "High",
    "completed": false,
    "due_date": "2026-09-25",
    "created_at": "2026-09-21T..."
  }
]

If there are no tasks:

[]
13. Get One Task
GET /tasks/<task_id>

Returns a single task.

Example
GET /tasks/1
Authentication

Required.

Authorization

The task must belong to the authenticated user.

If the task does not exist or belongs to another user:

Status: 404 Not Found

{
  "error": "Task not found"
}
Success Response

Status: 200 OK

{
  "id": 1,
  "user_id": 2,
  "title": "Complete DBMS revision",
  "description": "Revise joins",
  "priority": "High",
  "completed": false,
  "due_date": "2026-09-25",
  "created_at": "2026-09-21T..."
}
14. Update Task
PUT /tasks/<task_id>

Updates an existing task.

Example
PUT /tasks/1
Authentication

Required.

Request Body
{
  "title": "Complete DBMS and OS revision",
  "description": "Revise joins, processes and scheduling",
  "priority": "High",
  "completed": true,
  "due_date": "2026-09-26"
}
Supported Fields
title
description
priority
completed
due_date
Validation
Title
Must be a string.
Cannot be empty.
Maximum 100 characters.
Description

Must be a string if provided.

It may also be:

null
Priority

Must be one of:

Low
Medium
High
Completed

Must be a boolean:

true

or:

false
Due Date

Must use:

YYYY-MM-DD

or:

null
Authorization

Users can update only their own tasks.

Success Response

Status: 200 OK

{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "user_id": 2,
    "title": "Complete DBMS and OS revision",
    "description": "Revise joins, processes and scheduling",
    "priority": "High",
    "completed": true,
    "due_date": "2026-09-26",
    "created_at": "2026-09-21T..."
  }
}
15. Delete Task
DELETE /tasks/<task_id>

Deletes a task belonging to the authenticated user.

Example
DELETE /tasks/1
Authentication

Required.

Authorization

Users can delete only their own tasks.

Success Response

Status: 200 OK

{
  "message": "Task deleted successfully"
}

If the task does not exist or belongs to another user:

Status: 404 Not Found

{
  "error": "Task not found"
}
16. Admin Login
POST /admin/login

Authenticates an administrator.

Authentication

None.

Request Body
{
  "email": "admin@example.com",
  "password": "adminpassword"
}
Validation
Email is required.
Password is required.
Email must have a valid email format.
Password must contain at least 8 characters.
The account must exist.
The account must be active.

The account must have:

role = admin

Non-Admin Users

If a normal user attempts to log in through this endpoint:

Status: 403 Forbidden

{
  "error": "Admin access required"
}
Disabled Admin

If the admin account is disabled:

Status: 403 Forbidden

{
  "error": "Admin account is disabled"
}
Success Response

Status: 200 OK

{
  "message": "Admin login successful",
  "token": "<JWT_TOKEN>",
  "admin_id": 1,
  "username": "Admin",
  "email": "admin@example.com",
  "role": "admin"
}
17. Get All Users
GET /admin/users

Returns all registered users.

Authentication

Required.

Authorization

Admin only.

Authorization: Bearer <ADMIN_JWT_TOKEN>
Success Response

Status: 200 OK

[
  {
    "id": 1,
    "username": "Admin",
    "email": "admin@example.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-09-21T..."
  },
  {
    "id": 2,
    "username": "Sneha",
    "email": "sneha@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-09-21T..."
  }
]
18. Update User
PUT /admin/users/<user_id>

Allows an administrator to update a user's account.

Authentication

Required.

Authorization

Admin only.

Example
PUT /admin/users/2
Request Body

Any supported combination of:

{
  "username": "SnehaUpdated",
  "email": "updated@example.com",
  "role": "admin",
  "is_active": false
}
Supported Fields
username
email
role
is_active
Validation
Username
Must be a string.
Must contain 3–50 characters.
Must be unique.
Email
Must have a valid email format.
Must be unique.
Role

Must be:

user

or:

admin
is_active

Must be a boolean:

true

or:

false
Success Response

Status: 200 OK

{
  "message": "User updated successfully",
  "user": {
    "id": 2,
    "username": "SnehaUpdated",
    "email": "updated@example.com",
    "role": "admin",
    "is_active": false,
    "created_at": "2026-09-21T..."
  }
}
19. Delete User
DELETE /admin/users/<user_id>

Deletes a user account.

Authentication

Required.

Authorization

Admin only.

Example
DELETE /admin/users/2
Important Rule

An administrator cannot delete their own account.

Attempting to do so returns:

Status: 403 Forbidden

{
  "error": "Admin cannot delete their own account"
}
Success Response

Status: 200 OK

{
  "message": "User deleted successfully"
}
20. Get All Tasks as Admin
GET /admin/tasks

Returns all tasks in the system.

Authentication

Required.

Authorization

Admin only.

Request
GET /admin/tasks

No admin_id query parameter is required.

Success Response

Status: 200 OK

[
  {
    "id": 1,
    "user_id": 2,
    "title": "Complete DBMS revision",
    "description": "Revise joins",
    "priority": "High",
    "completed": false,
    "due_date": "2026-09-25",
    "created_at": "2026-09-21T..."
  }
]
21. Task Object

A task is represented using:

{
  "id": 1,
  "user_id": 2,
  "title": "Complete DBMS revision",
  "description": "Revise joins",
  "priority": "High",
  "completed": false,
  "due_date": "2026-09-25",
  "created_at": "2026-09-21T..."
}
Fields
Field	Description
id	Unique task ID
user_id	ID of the user who owns the task
title	Task title
description	Optional task description
priority	Low, Medium, or High
completed	Whether the task is completed
due_date	Optional due date
created_at	Task creation timestamp
22. User Object

A user is represented using:

{
  "id": 1,
  "username": "Sneha",
  "email": "sneha@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2026-09-21T..."
}
Fields
Field	Description
id	Unique user ID
username	Username
email	User email
role	user or admin
is_active	Whether the account is active
created_at	Account creation timestamp

Passwords are not returned in API responses.

23. Validation Rules

The backend performs server-side validation even if the frontend also validates user input.

This prevents clients from bypassing validation by directly calling the API.

Examples:

Invalid email → rejected
Short password → rejected
Invalid priority → rejected
Invalid role → rejected
Invalid date → rejected
Invalid boolean → rejected
Duplicate username → rejected
Duplicate email → rejected
24. HTTP Status Codes

The API uses standard HTTP status codes.

Status	Meaning
200	Successful request
201	Resource successfully created
400	Invalid request or validation error
401	Authentication failed or token missing/invalid
403	Authenticated but not authorized
404	Resource not found
409	Resource conflict, such as duplicate username/email
25. Security

The backend implements several security mechanisms.

Password Hashing

Passwords are not stored as plain text.

They are hashed using Werkzeug's password hashing functions.

The database therefore stores a password hash rather than the original password.

JWT Authentication

Protected endpoints require a valid JWT.

The token identifies the authenticated user.

Role-Based Authorization

Admin endpoints use admin authorization.

For example:

/admin/users
/admin/tasks

require an administrator.

Task Ownership

Normal users cannot access another user's tasks.

The backend verifies ownership using the authenticated user's ID.

Environment Variables

Sensitive configuration such as:

SECRET_KEY

is stored in the .env file rather than directly in source code.

The .env file is excluded from Git using .gitignore.

26. CORS

The backend allows requests from the frontend development origin:

http://localhost:5173

This is required because the React frontend and Flask backend run on different development servers.

The frontend communicates with Flask using HTTP requests.

If Vite runs on another port during development, such as 5174, the backend CORS configuration may need to be updated accordingly.

27. Example User Flow

A normal user interaction looks like:

1. User signs up
       ↓
2. User logs in
       ↓
3. Backend verifies credentials
       ↓
4. Backend returns JWT
       ↓
5. Frontend stores JWT
       ↓
6. Frontend sends JWT with task requests
       ↓
7. Backend validates JWT
       ↓
8. Backend identifies the user
       ↓
9. Backend performs the requested task operation
       ↓
10. Backend returns JSON response
28. Example Admin Flow

An administrator interaction looks like:

1. Admin logs in through /admin/login
       ↓
2. Backend verifies credentials
       ↓
3. Backend verifies role = admin
       ↓
4. Backend returns JWT
       ↓
5. Frontend stores JWT
       ↓
6. Admin accesses admin dashboard
       ↓
7. Frontend requests /admin/users or /admin/tasks
       ↓
8. Backend validates JWT
       ↓
9. Backend verifies admin role
       ↓
10. Backend performs admin operation
       ↓
11. Backend returns JSON response
29. Testing

The backend contains automated tests using pytest.

Current backend test status:

55 / 55 tests passed

The frontend also contains automated tests using Vitest and React Testing Library.

Current frontend test status:

13 / 13 tests passed

The tests cover authentication, task operations, admin operations, API behavior, and frontend routing/authentication behavior.

30. Running the Backend

Activate the virtual environment:

.venv\Scripts\activate

Start Flask:

python app.py

The backend is then available at:

http://127.0.0.1:5000
31. Architecture Summary

The application follows a client-server architecture:

React Frontend
      |
      | HTTP / JSON
      ↓
Flask REST API
      |
      | SQLAlchemy
      ↓
SQLite Database

Authentication and authorization are handled by the Flask backend.

The React frontend is responsible for the user interface and sending API requests.

The database stores users and tasks.

32. API Design Principles

The API follows several important principles.

Resource-Based URLs

Examples:

/tasks
/tasks/1
/admin/users
/admin/users/1
/admin/tasks
HTTP Methods Represent Operations
GET     → Read
POST    → Create
PUT     → Update
DELETE  → Delete
JSON Communication

Requests and responses use JSON.

Authentication Through JWT

Protected endpoints receive the token through the HTTP Authorization header.

Authorization on the Server

The frontend does not decide whether a user is an admin.

The backend verifies the user's role.

Ownership Enforcement

The backend determines which tasks a normal user is allowed to access.

This prevents users from simply changing an ID in a frontend request to access another user's data.