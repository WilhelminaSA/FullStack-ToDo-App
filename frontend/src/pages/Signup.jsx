import { useState } from 'react'
import {
  Link,
  useNavigate
} from 'react-router-dom'

import { signup } from '../api/api'

function Signup() {
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      await signup({
        username,
        email,
        password
      })

      navigate('/login')
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-card">
        <h1>Create Account</h1>

        <p className="auth-subtitle">
          Create your To-Do account
        </p>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>
              Username
            </label>

            <input
              type="text"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              placeholder="Enter your username"
              required
            />
          </div>

          <div className="form-group">
            <label>
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label>
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Create a password"
              required
            />
          </div>

          <button
            type="submit"
            className="full-width-button"
            disabled={loading}
          >
            {loading
              ? 'Creating account...'
              : 'Sign Up'}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{' '}

          <Link to="/login">
            Login
          </Link>
        </p>
      </div>
    </main>
  )
}

export default Signup