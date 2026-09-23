import {
  createContext,
  useContext,
  useState
} from 'react'

import {
  adminLogin as adminLoginRequest,
  login as loginRequest
} from '../api/api'

const AuthContext = createContext()

function getStoredUser() {
  const savedUser =
    localStorage.getItem('user')

  if (!savedUser) {
    return null
  }

  try {
    return JSON.parse(savedUser)
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    localStorage.getItem('token')
  )

  const [user, setUser] = useState(
    getStoredUser
  )

  async function login(email, password) {
    const data = await loginRequest({
      email,
      password
    })

    const receivedToken =
      data.access_token ||
      data.token

    if (!receivedToken) {
      throw new Error(
        'Login succeeded but no token was returned'
      )
    }

    const receivedUser =
      data.user ||
      {
        id: data.user_id,
        username: data.username,
        email: data.email,
        role: data.role || 'user'
      }

    localStorage.setItem(
      'token',
      receivedToken
    )

    localStorage.setItem(
      'user',
      JSON.stringify(receivedUser)
    )

    setToken(receivedToken)
    setUser(receivedUser)

    return data
  }

  async function adminLogin(email, password) {
    const data = await adminLoginRequest({
      email,
      password
    })

    if (!data.token) {
      throw new Error(
        'Admin login succeeded but no token was returned'
      )
    }

    const adminUser = {
      id: data.admin_id,
      username: 'Admin',
      email,
      role: 'admin'
    }

    localStorage.setItem(
      'token',
      data.token
    )

    localStorage.setItem(
      'user',
      JSON.stringify(adminUser)
    )

    setToken(data.token)
    setUser(adminUser)

    return data
  }

  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        adminLogin,
        logout,
        isAuthenticated: Boolean(token),
        isAdmin: user?.role === 'admin'
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}