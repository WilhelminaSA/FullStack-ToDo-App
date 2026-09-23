import {
  beforeEach,
  describe,
  expect,
  it,
  vi
} from 'vitest'

import {
  adminLogin,
  getAdminUsers,
  updateAdminUser,
  deleteAdminUser,
  getAdminTasks
} from '../api/api'

describe(
  'Admin API functions',
  () => {
    beforeEach(() => {
      localStorage.clear()

      global.fetch = vi.fn()
    })

    it(
      'sends admin login request',
      async () => {
        fetch.mockResolvedValue({
          ok: true,
          json: async () => ({
            token: 'admin-token',
            admin_id: 1
          })
        })

        await adminLogin({
          email: 'admin@example.com',
          password: 'password'
        })

        expect(
          fetch
        ).toHaveBeenCalledWith(
          'http://127.0.0.1:5000/admin/login',
          expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({
              email: 'admin@example.com',
              password: 'password'
            })
          })
        )
      }
    )

    it(
      'gets admin users',
      async () => {
        localStorage.setItem(
          'token',
          'admin-token'
        )

        fetch.mockResolvedValue({
          ok: true,
          json: async () => []
        })

        await getAdminUsers()

        expect(
          fetch
        ).toHaveBeenCalledWith(
          'http://127.0.0.1:5000/admin/users',
          expect.objectContaining({
            headers: expect.objectContaining({
              Authorization:
                'Bearer admin-token'
            })
          })
        )
      }
    )

    it(
      'updates an admin user',
      async () => {
        localStorage.setItem(
          'token',
          'admin-token'
        )

        fetch.mockResolvedValue({
          ok: true,
          json: async () => ({
            message:
              'User updated successfully'
          })
        })

        await updateAdminUser(
          5,
          {
            username: 'UpdatedUser',
            email: 'updated@example.com',
            is_admin: false,
            is_active: true
          }
        )

        expect(
          fetch
        ).toHaveBeenCalledWith(
          'http://127.0.0.1:5000/admin/users/5',
          expect.objectContaining({
            method: 'PUT'
          })
        )
      }
    )

    it(
      'deletes an admin user',
      async () => {
        localStorage.setItem(
          'token',
          'admin-token'
        )

        fetch.mockResolvedValue({
          ok: true,
          json: async () => ({
            message:
              'User deleted successfully'
          })
        })

        await deleteAdminUser(5)

        expect(
          fetch
        ).toHaveBeenCalledWith(
          'http://127.0.0.1:5000/admin/users/5',
          expect.objectContaining({
            method: 'DELETE'
          })
        )
      }
    )

    it(
      'gets admin tasks',
      async () => {
        localStorage.setItem(
          'token',
          'admin-token'
        )

        fetch.mockResolvedValue({
          ok: true,
          json: async () => []
        })

        await getAdminTasks(1)

        expect(
          fetch
        ).toHaveBeenCalledWith(
          'http://127.0.0.1:5000/admin/tasks?admin_id=1',
          expect.objectContaining({
            headers: expect.objectContaining({
              Authorization:
                'Bearer admin-token'
            })
          })
        )
      }
    )
  }
)