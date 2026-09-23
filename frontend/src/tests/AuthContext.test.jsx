import {
  beforeEach,
  describe,
  expect,
  it,
  vi
} from 'vitest'

import {
  renderHook,
  act
} from '@testing-library/react'

import {
  AuthProvider,
  useAuth
} from '../context/AuthContext'

import {
  login,
  adminLogin
} from '../api/api'

vi.mock('../api/api', () => ({
  login: vi.fn(),
  adminLogin: vi.fn()
}))

describe(
  'AuthContext',
  () => {
    beforeEach(() => {
      localStorage.clear()
      vi.clearAllMocks()
    })

    it(
      'starts unauthenticated',
      () => {
        const {
          result
        } = renderHook(
          () => useAuth(),
          {
            wrapper:
              AuthProvider
          }
        )

        expect(
          result.current.isAuthenticated
        ).toBe(false)

        expect(
          result.current.isAdmin
        ).toBe(false)

        expect(
          result.current.user
        ).toBeNull()
      }
    )

    it(
      'stores normal user after login',
      async () => {
        login.mockResolvedValue({
          token: 'user-token',
          user_id: 5,
          username: 'Sneha',
          email: 'sneha@example.com',
          role: 'user'
        })

        const {
          result
        } = renderHook(
          () => useAuth(),
          {
            wrapper:
              AuthProvider
          }
        )

        await act(
          async () => {
            await result.current.login(
              'sneha@example.com',
              'password'
            )
          }
        )

        expect(
          result.current.isAuthenticated
        ).toBe(true)

        expect(
          result.current.isAdmin
        ).toBe(false)

        expect(
          result.current.user.username
        ).toBe('Sneha')

        expect(
          localStorage.getItem('token')
        ).toBe('user-token')
      }
      )

    it(
      'stores admin after admin login',
      async () => {
        adminLogin.mockResolvedValue({
          token: 'admin-token',
          admin_id: 10
        })

        const {
          result
        } = renderHook(
          () => useAuth(),
          {
            wrapper:
              AuthProvider
          }
        )

        await act(
          async () => {
            await result.current.adminLogin(
              'admin@example.com',
              'password'
            )
          }
        )

        expect(
          result.current.isAuthenticated
        ).toBe(true)

        expect(
          result.current.isAdmin
        ).toBe(true)

        expect(
          result.current.user.role
        ).toBe('admin')

        expect(
          localStorage.getItem('token')
        ).toBe('admin-token')
      }
      )

    it(
      'clears authentication during logout',
      async () => {
        localStorage.setItem(
          'token',
          'token'
        )

        localStorage.setItem(
          'user',
          JSON.stringify({
            id: 1,
            username: 'User',
            email: 'user@example.com',
            role: 'user'
          })
        )

        const {
          result
        } = renderHook(
          () => useAuth(),
          {
            wrapper:
              AuthProvider
          }
        )

        expect(
          result.current.isAuthenticated
        ).toBe(true)

        act(() => {
          result.current.logout()
        })

        expect(
          result.current.isAuthenticated
        ).toBe(false)

        expect(
          result.current.user
        ).toBeNull()

        expect(
          localStorage.getItem('token')
        ).toBeNull()

        expect(
          localStorage.getItem('user')
        ).toBeNull()
      }
      )
  }
)