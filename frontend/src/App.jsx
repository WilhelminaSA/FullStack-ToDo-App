import {
  Navigate,
  Route,
  Routes
} from 'react-router-dom'

import { useAuth } from './context/AuthContext'

import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import AdminLogin from './pages/AdminLogin'
import AdminDashboard from './pages/AdminDashboard'

function ProtectedRoute({ children }) {
  const {
    isAuthenticated,
    isAdmin
  } = useAuth()

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
      />
    )
  }

  if (isAdmin) {
    return (
      <Navigate
        to="/admin/dashboard"
        replace
      />
    )
  }

  return children
}

function AdminRoute({ children }) {
  const {
    isAuthenticated,
    isAdmin
  } = useAuth()

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/admin/login"
        replace
      />
    )
  }

  if (!isAdmin) {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    )
  }

  return children
}

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />

      {/* USER ROUTES */}

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/signup"
        element={<Signup />}
      />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      {/* ADMIN ROUTES */}

      <Route
        path="/admin/login"
        element={<AdminLogin />}
      />

      <Route
        path="/admin/dashboard"
        element={
          <AdminRoute>
            <AdminDashboard />
          </AdminRoute>
        }
      />

      {/* FALLBACK */}

      <Route
        path="*"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />
    </Routes>
  )
}

export default App