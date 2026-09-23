import { useEffect, useMemo, useState } from 'react'
import { Navigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

import {
  deleteAdminUser,
  deleteTask,
  getAdminTasks,
  getAdminUsers,
  updateAdminUser
} from '../api/api'

import '../styles/admin.css'

function AdminDashboard() {
  const {
    user,
    logout,
    isAdmin
  } = useAuth()

  const [users, setUsers] = useState([])
  const [tasks, setTasks] = useState([])

  const [loadingUsers, setLoadingUsers] =
    useState(true)

  const [loadingTasks, setLoadingTasks] =
    useState(true)

  const [error, setError] = useState('')

  const [activeSection, setActiveSection] =
    useState('overview')

  const [userSearch, setUserSearch] =
    useState('')

  const [taskSearch, setTaskSearch] =
    useState('')

  const [updatingUserId, setUpdatingUserId] =
    useState(null)

  const [deletingUserId, setDeletingUserId] =
    useState(null)

  const [deletingTaskId, setDeletingTaskId] =
    useState(null)

  useEffect(() => {
    if (!isAdmin) {
      return
    }

    loadUsers()
    loadTasks()
  }, [isAdmin])

  if (!isAdmin) {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    )
  }

  async function loadUsers() {
    setLoadingUsers(true)
    setError('')

    try {
      const data =
        await getAdminUsers()

      setUsers(
        Array.isArray(data)
          ? data
          : []
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setLoadingUsers(false)
    }
  }

  async function loadTasks() {
    setLoadingTasks(true)
    setError('')

    try {
      const data =
        await getAdminTasks(user.id)

      setTasks(
        Array.isArray(data)
          ? data
          : []
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setLoadingTasks(false)
    }
  }

  async function handleToggleUserStatus(currentUser) {
    setUpdatingUserId(currentUser.id)
    setError('')

    try {
      await updateAdminUser(
        currentUser.id,
        {
          username: currentUser.username,
          email: currentUser.email,
          is_admin:
            currentUser.is_admin,
          is_active:
            !currentUser.is_active
        }
      )

      setUsers((previousUsers) =>
        previousUsers.map((item) =>
          item.id === currentUser.id
            ? {
                ...item,
                is_active:
                  !item.is_active
              }
            : item
        )
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setUpdatingUserId(null)
    }
  }

  async function handleToggleAdminRole(currentUser) {
    setUpdatingUserId(currentUser.id)
    setError('')

    try {
      await updateAdminUser(
        currentUser.id,
        {
          username: currentUser.username,
          email: currentUser.email,
          is_admin:
            !currentUser.is_admin,
          is_active:
            currentUser.is_active
        }
      )

      setUsers((previousUsers) =>
        previousUsers.map((item) =>
          item.id === currentUser.id
            ? {
                ...item,
                is_admin:
                  !item.is_admin
              }
            : item
        )
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setUpdatingUserId(null)
    }
  }

  async function handleDeleteUser(userId) {
    const shouldDelete =
      window.confirm(
        'Are you sure you want to delete this user?'
      )

    if (!shouldDelete) {
      return
    }

    setDeletingUserId(userId)
    setError('')

    try {
      await deleteAdminUser(userId)

      setUsers((previousUsers) =>
        previousUsers.filter(
          (item) =>
            item.id !== userId
        )
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setDeletingUserId(null)
    }
  }

  async function handleDeleteTask(taskId) {
    const shouldDelete =
      window.confirm(
        'Are you sure you want to delete this task?'
      )

    if (!shouldDelete) {
      return
    }

    setDeletingTaskId(taskId)
    setError('')

    try {
      await deleteTask(taskId)

      setTasks((previousTasks) =>
        previousTasks.filter(
          (task) =>
            task.id !== taskId
        )
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setDeletingTaskId(null)
    }
  }

  const filteredUsers = useMemo(() => {
    const search =
      userSearch
        .trim()
        .toLowerCase()

    if (!search) {
      return users
    }

    return users.filter((item) =>
      [
        item.username,
        item.email
      ]
        .filter(Boolean)
        .some((value) =>
          value
            .toLowerCase()
            .includes(search)
        )
    )
  }, [users, userSearch])

  const filteredTasks = useMemo(() => {
    const search =
      taskSearch
        .trim()
        .toLowerCase()

    if (!search) {
      return tasks
    }

    return tasks.filter((task) =>
      [
        task.title,
        task.description,
        String(task.user_id)
      ]
        .filter(Boolean)
        .some((value) =>
          value
            .toLowerCase()
            .includes(search)
        )
    )
  }, [tasks, taskSearch])

  const activeUsers =
    users.filter(
      (item) => item.is_active
    ).length

  const adminUsers =
    users.filter(
      (item) => item.is_admin
    ).length

  const completedTasks =
    tasks.filter(
      (task) => task.completed
    ).length

  return (
    <div className="admin-page">
      <header className="admin-header">
        <div>
          <p className="admin-eyebrow">
            ADMIN PANEL
          </p>

          <h1>
            To-Do Administration
          </h1>

          <p>
            Manage users and tasks
          </p>
        </div>

        <button
          className="admin-logout-button"
          onClick={logout}
        >
          Logout
        </button>
      </header>

      {error && (
        <div className="error-message admin-error">
          <span>{error}</span>

          <button
            className="dismiss-error"
            onClick={() =>
              setError('')
            }
          >
            ×
          </button>
        </div>
      )}

      <main className="admin-main">
        <nav className="admin-navigation">
          <button
            className={
              activeSection === 'overview'
                ? 'active'
                : ''
            }
            onClick={() =>
              setActiveSection('overview')
            }
          >
            Overview
          </button>

          <button
            className={
              activeSection === 'users'
                ? 'active'
                : ''
            }
            onClick={() =>
              setActiveSection('users')
            }
          >
            Users
          </button>

          <button
            className={
              activeSection === 'tasks'
                ? 'active'
                : ''
            }
            onClick={() =>
              setActiveSection('tasks')
            }
          >
            Tasks
          </button>
        </nav>

        {activeSection === 'overview' && (
          <section>
            <div className="admin-section-heading">
              <div>
                <p className="admin-eyebrow">
                  OVERVIEW
                </p>

                <h2>
                  System summary
                </h2>
              </div>
            </div>

            <div className="admin-stats">
              <div className="admin-stat-card">
                <span>
                  Total Users
                </span>

                <strong>
                  {users.length}
                </strong>
              </div>

              <div className="admin-stat-card">
                <span>
                  Active Users
                </span>

                <strong>
                  {activeUsers}
                </strong>
              </div>

              <div className="admin-stat-card">
                <span>
                  Admins
                </span>

                <strong>
                  {adminUsers}
                </strong>
              </div>

              <div className="admin-stat-card">
                <span>
                  Total Tasks
                </span>

                <strong>
                  {tasks.length}
                </strong>
              </div>

              <div className="admin-stat-card">
                <span>
                  Completed Tasks
                </span>

                <strong>
                  {completedTasks}
                </strong>
              </div>
            </div>

            <div className="admin-info-card">
              <h3>
                Admin controls
              </h3>

              <p>
                Use the Users section to manage
                accounts and the Tasks section to
                monitor tasks across the application.
              </p>
            </div>
          </section>
        )}

        {activeSection === 'users' && (
          <section>
            <div className="admin-section-heading">
              <div>
                <p className="admin-eyebrow">
                  USER MANAGEMENT
                </p>

                <h2>
                  Users
                </h2>
              </div>

              <input
                className="admin-search"
                type="search"
                value={userSearch}
                onChange={(event) =>
                  setUserSearch(
                    event.target.value
                  )
                }
                placeholder="Search users..."
              />
            </div>

            {loadingUsers ? (
              <div className="admin-loading">
                Loading users...
              </div>
            ) : filteredUsers.length === 0 ? (
              <div className="admin-empty">
                No users found.
              </div>
            ) : (
              <div className="admin-table-wrapper">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredUsers.map(
                      (item) => (
                        <tr key={item.id}>
                          <td>
                            {item.id}
                          </td>

                          <td>
                            {item.username}
                          </td>

                          <td>
                            {item.email}
                          </td>

                          <td>
                            <span
                              className={
                                item.is_admin
                                  ? 'admin-role-badge admin-role'
                                  : 'admin-role-badge user-role'
                              }
                            >
                              {item.is_admin
                                ? 'Admin'
                                : 'User'}
                            </span>
                          </td>

                          <td>
                            <span
                              className={
                                item.is_active
                                  ? 'admin-status active'
                                  : 'admin-status inactive'
                              }
                            >
                              {item.is_active
                                ? 'Active'
                                : 'Inactive'}
                            </span>
                          </td>

                          <td>
                            <div className="admin-action-group">
                              <button
                                type="button"
                                className="admin-small-button"
                                disabled={
                                  updatingUserId ===
                                  item.id
                                }
                                onClick={() =>
                                  handleToggleUserStatus(
                                    item
                                  )
                                }
                              >
                                {item.is_active
                                  ? 'Deactivate'
                                  : 'Activate'}
                              </button>

                              <button
                                type="button"
                                className="admin-small-button"
                                disabled={
                                  updatingUserId ===
                                  item.id
                                }
                                onClick={() =>
                                  handleToggleAdminRole(
                                    item
                                  )
                                }
                              >
                                {item.is_admin
                                  ? 'Remove Admin'
                                  : 'Make Admin'}
                              </button>

                              <button
                                type="button"
                                className="admin-small-button danger"
                                disabled={
                                  deletingUserId ===
                                  item.id
                                }
                                onClick={() =>
                                  handleDeleteUser(
                                    item.id
                                  )
                                }
                              >
                                {deletingUserId ===
                                item.id
                                  ? 'Deleting...'
                                  : 'Delete'}
                              </button>
                            </div>
                          </td>
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        )}

        {activeSection === 'tasks' && (
          <section>
            <div className="admin-section-heading">
              <div>
                <p className="admin-eyebrow">
                  TASK MANAGEMENT
                </p>

                <h2>
                  All Tasks
                </h2>
              </div>

              <input
                className="admin-search"
                type="search"
                value={taskSearch}
                onChange={(event) =>
                  setTaskSearch(
                    event.target.value
                  )
                }
                placeholder="Search tasks..."
              />
            </div>

            {loadingTasks ? (
              <div className="admin-loading">
                Loading tasks...
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="admin-empty">
                No tasks found.
              </div>
            ) : (
              <div className="admin-table-wrapper">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>User ID</th>
                      <th>Title</th>
                      <th>Priority</th>
                      <th>Due Date</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredTasks.map(
                      (task) => (
                        <tr key={task.id}>
                          <td>
                            {task.id}
                          </td>

                          <td>
                            {task.user_id}
                          </td>

                          <td>
                            <strong>
                              {task.title}
                            </strong>

                            {task.description && (
                              <div className="admin-task-description">
                                {task.description}
                              </div>
                            )}
                          </td>

                          <td>
                            <span
                              className={`priority-badge priority-${task.priority?.toLowerCase()}`}
                            >
                              {task.priority}
                            </span>
                          </td>

                          <td>
                            {task.due_date ||
                              '—'}
                          </td>

                          <td>
                            <span
                              className={
                                task.completed
                                  ? 'admin-status active'
                                  : 'admin-status inactive'
                              }
                            >
                              {task.completed
                                ? 'Completed'
                                : 'Pending'}
                            </span>
                          </td>

                          <td>
                            <button
                              type="button"
                              className="admin-small-button danger"
                              disabled={
                                deletingTaskId ===
                                task.id
                              }
                              onClick={() =>
                                handleDeleteTask(
                                  task.id
                                )
                              }
                            >
                              {deletingTaskId ===
                              task.id
                                ? 'Deleting...'
                                : 'Delete'}
                            </button>
                          </td>
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default AdminDashboard