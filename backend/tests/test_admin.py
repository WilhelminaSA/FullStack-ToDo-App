from models import db, User, Task
from werkzeug.security import generate_password_hash


def test_admin_login_success(client):
    admin = User(
        username='adminuser',
        email='admin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    response = client.post(
        '/admin/login',
        json={
            'email': 'admin@example.com',
            'password': 'adminpass123'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data['message'] == 'Admin login successful'
    assert 'token' in data
    assert data['admin_id'] == admin.id


def test_admin_can_access_all_users(client):
    admin = User(
        username='adminusers',
        email='adminusers@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user = User(
        username='normalusers',
        email='normalusers@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'adminusers@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.get(
        '/admin/users',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)

    usernames = [user['username'] for user in data]

    assert 'adminusers' in usernames
    assert 'normalusers' in usernames


def test_normal_user_cannot_access_admin_users(client):
    user = User(
        username='regularuser',
        email='regularuser@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    login_response = client.post(
        '/login',
        json={
            'email': 'regularuser@example.com',
            'password': 'userpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.get(
        '/admin/users',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 403

    data = response.get_json()

    assert data['error'] == 'Admin access required'


def test_admin_can_update_user_role(client):
    admin = User(
        username='roleadmin',
        email='roleadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user = User(
        username='roleuser',
        email='roleuser@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'roleadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.put(
        f'/admin/users/{user.id}',
        json={
            'role': 'admin'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data['message'] == 'User updated successfully'

    updated_user = db.session.get(User, user.id)

    assert updated_user.role == 'admin'


def test_admin_can_access_all_tasks(client):
    admin = User(
        username='taskadmin',
        email='taskadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user1 = User(
        username='taskuser1',
        email='taskuser1@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    user2 = User(
        username='taskuser2',
        email='taskuser2@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    task1 = Task(
        user_id=user1.id,
        title='User 1 Task',
        description='Task created by user 1',
        priority='High'
    )

    task2 = Task(
        user_id=user2.id,
        title='User 2 Task',
        description='Task created by user 2',
        priority='Low'
    )

    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'taskadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.get(
        '/admin/tasks',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)

    titles = [task['title'] for task in data]

    assert 'User 1 Task' in titles
    assert 'User 2 Task' in titles


def test_admin_can_delete_user_and_user_tasks(client):
    admin = User(
        username='deleteadmin',
        email='deleteadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user = User(
        username='deleteuser',
        email='deleteuser@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

    task = Task(
        user_id=user.id,
        title='Task To Be Deleted',
        description='This task should be deleted with the user',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    user_id = user.id
    task_id = task.id

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'deleteadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.delete(
        f'/admin/users/{user_id}',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data['message'] == 'User deleted successfully'

    deleted_user = db.session.get(User, user_id)

    assert deleted_user is None

    deleted_task = db.session.get(Task, task_id)

    assert deleted_task is None


def test_admin_cannot_delete_themselves(client):
    admin = User(
        username='selfdeleteadmin',
        email='selfdeleteadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'selfdeleteadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.delete(
        f'/admin/users/{admin.id}',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 403

    data = response.get_json()

    assert data['error'] == 'Admin cannot delete their own account'

    existing_admin = db.session.get(User, admin.id)

    assert existing_admin is not None


# ---------------------------------------------------------
# Admin login validation tests
# ---------------------------------------------------------

def test_admin_login_rejects_normal_user(client):
    user = User(
        username='normaladminlogin',
        email='normaladminlogin@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    response = client.post(
        '/admin/login',
        json={
            'email': 'normaladminlogin@example.com',
            'password': 'userpass123'
        }
    )

    assert response.status_code == 403

    data = response.get_json()

    assert data['error'] == 'Admin access required'


def test_admin_login_rejects_disabled_admin(client):
    admin = User(
        username='disabledadmin',
        email='disabledadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=False
    )

    db.session.add(admin)
    db.session.commit()

    response = client.post(
        '/admin/login',
        json={
            'email': 'disabledadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert response.status_code == 403

    data = response.get_json()

    assert data['error'] == 'Admin account is disabled'


def test_admin_login_requires_request_body(client):
    response = client.post('/admin/login')

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Request body is required'


# ---------------------------------------------------------
# Admin user validation tests
# ---------------------------------------------------------

def test_admin_update_user_rejects_invalid_role(client):
    admin = User(
        username='invalidroleadmin',
        email='invalidroleadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user = User(
        username='invalidroleuser',
        email='invalidroleuser@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'invalidroleadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.put(
        f'/admin/users/{user.id}',
        json={
            'role': 'superadmin'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Role must be user or admin'


def test_admin_update_user_rejects_duplicate_username(client):
    admin = User(
        username='duplicateusernameadmin',
        email='duplicateusernameadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user1 = User(
        username='existingusername',
        email='existingusername@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    user2 = User(
        username='secondusername',
        email='secondusername@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'duplicateusernameadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.put(
        f'/admin/users/{user2.id}',
        json={
            'username': 'existingusername'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 409

    data = response.get_json()

    assert data['error'] == 'Username already exists'


def test_admin_update_user_rejects_duplicate_email(client):
    admin = User(
        username='duplicateemailadmin',
        email='duplicateemailadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    user1 = User(
        username='emailuser1',
        email='existingemail@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    user2 = User(
        username='emailuser2',
        email='secondemail@example.com',
        password_hash=generate_password_hash('userpass123'),
        role='user',
        is_active=True
    )

    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'duplicateemailadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.put(
        f'/admin/users/{user2.id}',
        json={
            'email': 'existingemail@example.com'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 409

    data = response.get_json()

    assert data['error'] == 'Email already exists'


def test_admin_update_nonexistent_user_returns_404(client):
    admin = User(
        username='missinguseradmin',
        email='missinguseradmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'missinguseradmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.put(
        '/admin/users/99999',
        json={
            'role': 'user'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data['error'] == 'User not found'


def test_admin_delete_nonexistent_user_returns_404(client):
    admin = User(
        username='missingdeleteadmin',
        email='missingdeleteadmin@example.com',
        password_hash=generate_password_hash('adminpass123'),
        role='admin',
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    login_response = client.post(
        '/admin/login',
        json={
            'email': 'missingdeleteadmin@example.com',
            'password': 'adminpass123'
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()['token']

    response = client.delete(
        '/admin/users/99999',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data['error'] == 'User not found'


def test_admin_protected_route_requires_authorization(client):
    response = client.get('/admin/users')

    assert response.status_code == 401

    data = response.get_json()

    assert data['error'] == 'Authorization token is required'


def test_admin_protected_route_rejects_invalid_token(client):
    response = client.get(
        '/admin/users',
        headers={
            'Authorization': 'Bearer invalid.jwt.token'
        }
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data['error'] == 'Invalid token'