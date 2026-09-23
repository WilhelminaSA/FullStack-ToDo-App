import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../context/AuthContext'

import {
  createTask,
  deleteTask,
  getTasks,
  updateTask
} from '../api/api'

function Dashboard() {
  const { user, logout } = useAuth()

  const [tasks, setTasks] = useState([])

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [deletingTaskId, setDeletingTaskId] = useState(null)
  const [error, setError] = useState('')

  const [showForm, setShowForm] = useState(false)
  const [editingTaskId, setEditingTaskId] = useState(null)

  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium',
    due_date: ''
  })

  const [statusFilter, setStatusFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')

  useEffect(() => {
    loadTasks()
  }, [])

  async function loadTasks() {
    setLoading(true)
    setError('')

    try {
      const data = await getTasks()

      // Backend returns the task array directly.
      setTasks(Array.isArray(data) ? data : [])
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  function resetForm() {
    setNewTask({
      title: '',
      description: '',
      priority: 'medium',
      due_date: ''
    })

    setEditingTaskId(null)
    setShowForm(false)
  }

  function handleInputChange(event) {
    const { name, value } = event.target

    setNewTask((previousTask) => ({
      ...previousTask,
      [name]: value
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!newTask.title.trim()) {
      setError('Task title is required.')
      return
    }

    setSaving(true)
    setError('')

    try {
      if (editingTaskId) {
        const data = await updateTask(
          editingTaskId,
          newTask
        )

        const updatedTask =
          data.task || data

        setTasks((previousTasks) =>
          previousTasks.map((task) =>
            task.id === editingTaskId
              ? updatedTask
              : task
          )
        )
      } else {
        const data = await createTask(newTask)

        // Backend returns task_id instead of id.
        const createdTask = {
          id: data.task_id,
          user_id: data.user_id,
          title: data.title,
          description: data.description,
          priority: data.priority,
          completed: data.completed,
          due_date: data.due_date,
          created_at: data.created_at
        }

        setTasks((previousTasks) => [
          createdTask,
          ...previousTasks
        ])
      }

      resetForm()
    } catch (error) {
      setError(error.message)
    } finally {
      setSaving(false)
    }
  }

  function handleEdit(task) {
    setEditingTaskId(task.id)

    setNewTask({
      title: task.title || '',
      description: task.description || '',
      priority: task.priority
        ? task.priority.toLowerCase()
        : 'medium',
      due_date: task.due_date || ''
    })

    setError('')
    setShowForm(true)

    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }

  async function handleToggleComplete(task) {
    setError('')

    try {
      const data = await updateTask(task.id, {
        title: task.title,
        description: task.description || '',
        priority: task.priority,
        completed: !task.completed,
        due_date: task.due_date || ''
      })

      const updatedTask =
        data.task || data

      setTasks((previousTasks) =>
        previousTasks.map((currentTask) =>
          currentTask.id === task.id
            ? updatedTask
            : currentTask
        )
      )
    } catch (error) {
      setError(error.message)
    }
  }

  async function handleDelete(taskId) {
    const shouldDelete = window.confirm(
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
          (task) => task.id !== taskId
        )
      )
    } catch (error) {
      setError(error.message)
    } finally {
      setDeletingTaskId(null)
    }
  }

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const matchesStatus =
        statusFilter === 'all' ||
        (statusFilter === 'completed' && task.completed) ||
        (statusFilter === 'pending' && !task.completed)

      // Backend sends High/Medium/Low.
      // Frontend filter values are high/medium/low.
      const matchesPriority =
        priorityFilter === 'all' ||
        task.priority?.toLowerCase() === priorityFilter

      return matchesStatus && matchesPriority
    })
  }, [
    tasks,
    statusFilter,
    priorityFilter
  ])

  const completedCount = tasks.filter(
    (task) => task.completed
  ).length

  const pendingCount =
    tasks.length - completedCount

  function formatDueDate(date) {
    if (!date) {
      return null
    }

    const formattedDate = new Date(date)

    if (Number.isNaN(formattedDate.getTime())) {
      return date
    }

    return formattedDate.toLocaleDateString(
      'en-IN',
      {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      }
    )
  }

  return (
    <>
      <header>
        <div className="dashboard-header">
          <div>
            <h1>My To-Do List</h1>

            <p className="welcome-text">
              Welcome back, {user?.username || 'User'} 👋
            </p>
          </div>

          <button
            className="logout-button"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </header>

      <main>
        {error && (
          <div className="error-message page-error">
            <span>{error}</span>

            <button
              className="dismiss-error"
              onClick={() => setError('')}
            >
              ×
            </button>
          </div>
        )}

        <section className="dashboard-overview">
          <div>
            <p className="dashboard-eyebrow">
              YOUR TASKS
            </p>

            <h2>
              Stay organized.
            </h2>

            <p className="dashboard-description">
              Keep track of what needs to get done
              and make progress one task at a time.
            </p>
          </div>

          <button
            className="add-task-button"
            onClick={() => {
              setError('')
              setEditingTaskId(null)
              setShowForm(true)
            }}
          >
            + Add Task
          </button>
        </section>

        <section className="task-stats">
          <div className="stat-card">
            <span className="stat-label">
              Total Tasks
            </span>

            <strong>
              {tasks.length}
            </strong>
          </div>

          <div className="stat-card">
            <span className="stat-label">
              Pending
            </span>

            <strong>
              {pendingCount}
            </strong>
          </div>

          <div className="stat-card">
            <span className="stat-label">
              Completed
            </span>

            <strong>
              {completedCount}
            </strong>
          </div>
        </section>

        {showForm && (
          <section className="task-form-section">
            <div className="form-heading">
              <div>
                <p className="form-eyebrow">
                  {editingTaskId
                    ? 'EDIT TASK'
                    : 'NEW TASK'}
                </p>

                <h2>
                  {editingTaskId
                    ? 'Update your task'
                    : 'Create a new task'}
                </h2>
              </div>

              <button
                type="button"
                className="close-form-button"
                onClick={resetForm}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="title">
                  Task title
                </label>

                <input
                  id="title"
                  name="title"
                  type="text"
                  value={newTask.title}
                  onChange={handleInputChange}
                  placeholder="e.g. Complete DBMS revision"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="description">
                  Description
                </label>

                <textarea
                  id="description"
                  name="description"
                  value={newTask.description}
                  onChange={handleInputChange}
                  placeholder="Add some details about this task..."
                  rows="3"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="priority">
                    Priority
                  </label>

                  <select
                    id="priority"
                    name="priority"
                    value={newTask.priority}
                    onChange={handleInputChange}
                  >
                    <option value="low">
                      Low
                    </option>

                    <option value="medium">
                      Medium
                    </option>

                    <option value="high">
                      High
                    </option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="due_date">
                    Due date
                  </label>

                  <input
                    id="due_date"
                    name="due_date"
                    type="date"
                    value={newTask.due_date}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-buttons">
                <button
                  type="submit"
                  disabled={saving}
                >
                  {saving
                    ? editingTaskId
                      ? 'Saving changes...'
                      : 'Creating task...'
                    : editingTaskId
                      ? 'Save Changes'
                      : 'Create Task'}
                </button>

                <button
                  type="button"
                  className="cancel-button"
                  onClick={resetForm}
                  disabled={saving}
                >
                  Cancel
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="tasks-section">
          <div className="section-heading">
            <div>
              <p className="section-eyebrow">
                TASK LIST
              </p>

              <h2>
                Your tasks
              </h2>
            </div>

            {!loading && tasks.length > 0 && (
              <span className="task-count">
                {filteredTasks.length}{' '}
                {filteredTasks.length === 1
                  ? 'task'
                  : 'tasks'}
              </span>
            )}
          </div>

          <div className="filters">
            <div className="filter-group">
              <label htmlFor="status-filter">
                Status
              </label>

              <select
                id="status-filter"
                value={statusFilter}
                onChange={(event) =>
                  setStatusFilter(event.target.value)
                }
              >
                <option value="all">
                  All
                </option>

                <option value="pending">
                  Pending
                </option>

                <option value="completed">
                  Completed
                </option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="priority-filter">
                Priority
              </label>

              <select
                id="priority-filter"
                value={priorityFilter}
                onChange={(event) =>
                  setPriorityFilter(event.target.value)
                }
              >
                <option value="all">
                  All
                </option>

                <option value="high">
                  High
                </option>

                <option value="medium">
                  Medium
                </option>

                <option value="low">
                  Low
                </option>
              </select>
            </div>
          </div>

          {loading ? (
            <div className="loading-container">
              <div className="spinner"></div>

              <p>
                Loading your tasks...
              </p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="empty-state empty-state-main">
              <div className="empty-icon">
                ✓
              </div>

              <h3>
                Your task list is empty
              </h3>

              <p>
                You don't have any tasks yet.
                Create your first task and start
                getting things done.
              </p>

              <button
                onClick={() => {
                  setError('')
                  setShowForm(true)
                }}
              >
                + Create Your First Task
              </button>
            </div>
          ) : filteredTasks.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">
                🔎
              </div>

              <h3>
                No matching tasks
              </h3>

              <p>
                No tasks match your current filters.
                Try changing the status or priority
                filter.
              </p>

              <button
                className="secondary-button"
                onClick={() => {
                  setStatusFilter('all')
                  setPriorityFilter('all')
                }}
              >
                Clear Filters
              </button>
            </div>
          ) : (
            <div className="task-list">
              {filteredTasks.map((task) => (
                <article
                  key={task.id}
                  className={`task-card ${
                    task.completed
                      ? 'completed-task'
                      : ''
                  }`}
                >
                  <div className="task-card-top">
                    <button
                      type="button"
                      className={`complete-checkbox ${
                        task.completed
                          ? 'checked'
                          : ''
                      }`}
                      onClick={() =>
                        handleToggleComplete(task)
                      }
                      aria-label={
                        task.completed
                          ? 'Mark task as incomplete'
                          : 'Mark task as complete'
                      }
                    >
                      {task.completed && '✓'}
                    </button>

                    <div className="task-card-content">
                      <div className="task-title-row">
                        <h3>
                          {task.title}
                        </h3>

                        <span
                          className={`priority-badge priority-${task.priority?.toLowerCase()}`}
                        >
                          {task.priority}
                        </span>
                      </div>

                      {task.description && (
                        <p className="task-description">
                          {task.description}
                        </p>
                      )}

                      <div className="task-meta">
                        {task.due_date && (
                          <span>
                            📅 Due{' '}
                            {formatDueDate(
                              task.due_date
                            )}
                          </span>
                        )}

                        <span
                          className={
                            task.completed
                              ? 'status-complete'
                              : 'status-pending'
                          }
                        >
                          {task.completed
                            ? 'Completed'
                            : 'Pending'}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="task-card-actions">
                    <button
                      type="button"
                      className="edit-button"
                      onClick={() =>
                        handleEdit(task)
                      }
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      className="delete-button"
                      onClick={() =>
                        handleDelete(task.id)
                      }
                      disabled={
                        deletingTaskId === task.id
                      }
                    >
                      {deletingTaskId === task.id
                        ? 'Deleting...'
                        : 'Delete'}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </>
  )
}

export default Dashboard