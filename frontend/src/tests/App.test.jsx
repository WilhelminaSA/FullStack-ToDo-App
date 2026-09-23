import {
  beforeEach,
  describe,
  expect,
  it,
  vi
} from 'vitest'

import {
  render,
  screen,
  waitFor
} from '@testing-library/react'

import {
  MemoryRouter
} from 'react-router-dom'

import App from '../App'

import { AuthProvider } from '../context/AuthContext'

vi.mock('../api/api', () => ({
  login: vi.fn(),
  adminLogin: vi.fn(),
  signup: vi.fn(),
  getTasks: vi.fn(),
  createTask: vi.fn(),
  updateTask: vi.fn(),
  deleteTask: vi.fn(),
  getAdminUsers: vi.fn(),
  updateAdminUser: vi.fn(),
  deleteAdminUser: vi.fn(),
  getAdminTasks: vi.fn()
}))

describe(
  'Application routing',
  () => {
    beforeEach(() => {
      localStorage.clear()
    })

    it(
      'redirects unauthenticated users to login',
      () => {
        render(
          <MemoryRouter
            initialEntries={[
              '/dashboard'
            ]}
          >
            <AuthProvider>
              <App />
            </AuthProvider>
          </MemoryRouter>
        )

        expect(
          screen.getByRole(
            'heading',
            {
              name: 'Welcome Back'
            }
          )
        ).toBeInTheDocument()
      }
    )

    it(
      'renders admin login page',
      () => {
        render(
          <MemoryRouter
            initialEntries={[
              '/admin/login'
            ]}
          >
            <AuthProvider>
              <App />
            </AuthProvider>
          </MemoryRouter>
        )

        expect(
          screen.getByRole(
            'heading',
            {
              name: 'Admin Login'
            }
          )
        ).toBeInTheDocument()
      }
    )

    it(
      'redirects normal users away from admin dashboard',
      async () => {
        localStorage.setItem(
          'token',
          'user-token'
        )

        localStorage.setItem(
          'user',
          JSON.stringify({
            id: 1,
            username: 'TestUser',
            email: 'test@example.com',
            role: 'user'
          })
        )

        render(
          <MemoryRouter
            initialEntries={[
              '/admin/dashboard'
            ]}
          >
            <AuthProvider>
              <App />
            </AuthProvider>
          </MemoryRouter>
        )

        await waitFor(() => {
          expect(
            screen.getByRole(
              'heading',
              {
                name: 'My To-Do List'
              }
            )
          ).toBeInTheDocument()
        })
      }
    )

    it(
      'allows an admin to access admin dashboard',
      async () => {
        localStorage.setItem(
          'token',
          'admin-token'
        )

        localStorage.setItem(
          'user',
          JSON.stringify({
            id: 1,
            username: 'Admin',
            email: 'admin@example.com',
            role: 'admin'
          })
        )

        render(
          <MemoryRouter
            initialEntries={[
              '/admin/dashboard'
            ]}
          >
            <AuthProvider>
              <App />
            </AuthProvider>
          </MemoryRouter>
        )

        await waitFor(() => {
          expect(
            screen.getByRole(
              'heading',
              {
                name: 'To-Do Administration'
              }
            )
          ).toBeInTheDocument()
        })
      }
    )
  }
)