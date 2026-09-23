# ✨ To-Do List App – Feature List

This file outlines all the core features available in the backend of the To-Do List Manager.

---

## 🔹 USER FEATURES

1. **Sign Up**
   - Allows new users to register using username, email, and password.
2. **Login**
   - Secure login using email and password.
   - Issues JWT token for session management.
3. **Create Task**
   - Users can create a task with title, description, due date, and priority.
4. **View Tasks**
   - Users can view all their tasks.
   - Filtering options:
     - By priority (Low, Medium, High)
     - By status (Completed or Not Completed)
5. **Update Task**
   - Edit existing task's title, completion status, priority, or due date.
6. **Delete Task**
   - Permanently delete any task owned by the user.

---

## 🔐 ADMIN FEATURES

1. **Admin Login**
   - Login with email/password and get a JWT token.
   - Used for accessing protected admin routes.
2. **View All Users**
   - Retrieve the list of all registered users.
3. **Update User Info**
   - Modify any user's:
     - Username
     - Email
     - Admin status
4. **Enable/Disable Users**
   - Temporarily deactivate or reactivate a user account.
5. **View All Tasks**
   - Access and view all tasks created by all users.