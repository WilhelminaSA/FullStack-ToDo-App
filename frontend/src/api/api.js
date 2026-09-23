const API_URL = import.meta.env.VITE_API_URL

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token')

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(
      data.message ||
      data.error ||
      'Something went wrong'
    )
  }

  return data
}

/* =========================
   USER AUTHENTICATION
========================= */

export async function signup(userData) {
  return apiRequest('/signup', {
    method: 'POST',
    body: JSON.stringify(userData)
  })
}

export async function login(credentials) {
  return apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify(credentials)
  })
}

/* =========================
   USER TASKS
========================= */

export async function getTasks() {
  return apiRequest('/tasks')
}

export async function createTask(taskData) {
  console.log(
    'CREATE TASK PAYLOAD:',
    taskData
  )

  const formattedTaskData = {
    ...taskData,
    priority:
      taskData.priority.charAt(0).toUpperCase() +
      taskData.priority.slice(1)
  }

  console.log(
    'FORMATTED CREATE TASK PAYLOAD:',
    formattedTaskData
  )

  return apiRequest('/tasks', {
    method: 'POST',
    body: JSON.stringify(formattedTaskData)
  })
}

export async function updateTask(taskId, taskData) {
  const formattedTaskData = {
    ...taskData,
    priority:
      taskData.priority.charAt(0).toUpperCase() +
      taskData.priority.slice(1)
  }

  return apiRequest(`/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(formattedTaskData)
  })
}

export async function deleteTask(taskId) {
  return apiRequest(`/tasks/${taskId}`, {
    method: 'DELETE'
  })
}

/* =========================
   ADMIN AUTHENTICATION
========================= */

export async function adminLogin(credentials) {
  return apiRequest('/admin/login', {
    method: 'POST',
    body: JSON.stringify(credentials)
  })
}

/* =========================
   ADMIN USER MANAGEMENT
========================= */

export async function getAdminUsers() {
  return apiRequest('/admin/users')
}

export async function updateAdminUser(userId, userData) {
  return apiRequest(`/admin/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(userData)
  })
}

export async function deleteAdminUser(userId) {
  return apiRequest(`/admin/users/${userId}`, {
    method: 'DELETE'
  })
}

/* =========================
   ADMIN TASK MANAGEMENT
========================= */

export async function getAdminTasks(adminId) {
  return apiRequest(
    `/admin/tasks?admin_id=${adminId}`
  )
}