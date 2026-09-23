
# 📝 To-Do List Backend with Admin Panel (Flask API)

## 📁 Project Structure

This project contains three main Python files:

- `app.py` – Main Flask app with user and task routes
- `models.py` – SQLAlchemy models (User, Task)
- `admin.py` – Blueprint routes for admin functionalities

---

## Documentation
- [Feature List](features.md) - Complete list of user and admin features

## 🔍 What This Project Does

This Flask-based backend API helps users manage daily tasks efficiently and securely. It supports two types of users:

- **Regular Users**:
  - Create accounts
  - Log in securely
  - Create, view, update, and delete tasks

- **Admins**:
  - Log in securely with admin privileges
  - View all registered users
  - Enable/disable user accounts
  - Update user details
  - View all tasks created by any user

---

## ✨ Key Features

### 🔹 User Features
1. **Sign Up** – Create a new user account  
2. **Login** – Secure login with email and password  
3. **Create Task** – Add task with title, description, priority, and due date  
4. **View Tasks** – With filters (completion or priority)  
5. **Update Task** – Change title, status, priority, or due date  
6. **Delete Task** – Remove task

### 🔹 Admin Features
1. **Admin Login** – Get JWT token  
2. **View All Users** – Admin-only access  
3. **Update User Info** – Change user details  
4. **Enable/Disable Users** – Temporarily deactivate or reactivate users  
5. **View All Tasks** – See tasks of all users

---

## 🛠️ Technology Stack

- **Backend**: Python (Flask)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: JWT (for Admin)
- **API Testing**: Postman

---

## 📬 API Testing with Postman (Open API Client)

**Postman** helps test REST APIs by sending HTTP requests (GET, POST, PUT, DELETE). With Postman you can:

- Test all endpoints
- Send JSON data in body
- Use query parameters and headers
- Add Bearer token for authentication

🧪 Download Postman collection here (if included):  
`ToDoListAPI.postman_collection.json`

---

## 🚀 API Functionalities & Endpoints

### 🔹 USER FEATURES

#### 🟢 1. Sign Up
- `POST` `/signup`  
```json
{
  "username": "john123",
  "email": "john@example.com",
  "password": "secretpass"
}
```

#### 🟢 2. Login
- `POST` `/login`  
```json
{
  "email": "john@example.com",
  "password": "secretpass"
}
```

#### 🟢 3. Create Task
- `POST` `/tasks`  
```json
{
  "user_id": 1,
  "title": "Finish assignment",
  "description": "MPMC project",
  "due_date": "2025-05-05",
  "priority": "High"
}
```

#### 🟢 4. Get Tasks (with filters)
- `GET`  
`/tasks?user_id=1&completed=false&priority=High`

#### 🟢 5. Update Task
- `/tasks/<task_id>`  
```json
{
  "title": "Finish Final Report",
  "completed": true,
  "priority": "Medium"
}
```

#### 🟢 6. Delete Task
- `/tasks/<task_id>`

---

### 🔐 ADMIN FEATURES

#### 🛡️ 1. Admin Login (Get Token)
- `POST` `/admin/login`  
```json
{
  "email": "admin@example.com",
  "password": "adminpass123"
}
```
🔑 Save the `token` from response for future requests.

#### 🛡️ 2. Get All Users
- `GET` `/admin/users`  
Header:  
```
Authorization: Bearer <your_token>
```

#### 🛡️ 3. Update User Info
- `PUT` `/admin/users/<user_id>`  
```json
{
  "username": "john_updated",
  "email": "john_updated@example.com",
  "is_admin": false
}
```

#### 🛡️ 4. Enable/Disable User
- `PUT` `/admin/users/<user_id>/status`  
Header:  
```
Authorization: Bearer <your_token>
```
Body:  
```json
{
  "is_active": false
}
```
(Use `true` to enable again.)

#### 🛡️ 5. View All Tasks
- `GET` `/admin/tasks?admin_id=<admin_id>`

---
## 📚 License

This project is built for educational purposes and can be reused with credit.
