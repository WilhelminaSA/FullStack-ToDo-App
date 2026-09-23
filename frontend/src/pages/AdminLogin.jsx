import { useState } from 'react'
import {
  Link,
  Navigate,
  useNavigate
} from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

function AdminLogin() {
  const navigate = useNavigate()

  const {
    adminLogin,
    isAuthenticated,
    isAdmin
  } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (isAuthenticated && isAdmin) {
    return (
      <Navigate
        to="/admin/dashboard"
        replace
      />
    )
  }

  if (isAuthenticated && !isAdmin) {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    )
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      await adminLogin(
        email,
        password
      )

      navigate('/admin/dashboard')
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="admin-auth-page">
      <div className="admin-auth-card">
        <div className="admin-badge">
          ADMIN
        </div>

        <h1>
          Admin Login
        </h1>

        <p className="auth-subtitle">
          Sign in to manage users and tasks
        </p>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="admin-email">
              Email
            </label>

            <input
              id="admin-email"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="Enter admin email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="admin-password">
              Password
            </label>

            <input
              id="admin-password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter admin password"
              required
            />
          </div>

          <button
            type="submit"
            className="full-width-button"
            disabled={loading}
          >
            {loading
              ? 'Logging in...'
              : 'Admin Login'}
          </button>
        </form>

        <p className="auth-footer">
          <Link to="/login">
            Back to user login
          </Link>
        </p>
      </div>
    </main>
  )
}

export default AdminLogin