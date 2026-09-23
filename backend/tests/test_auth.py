def test_home(client):
    response = client.get('/')

    assert response.status_code == 200

    data = response.get_json()

    assert data['message'] == 'Welcome to the To-Do List API'


def test_signup_success(client):
    response = client.post(
        '/signup',
        json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data['message'] == 'User created successfully'
    assert 'user_id' in data


def test_login_success(client):
    signup_response = client.post(
        '/signup',
        json={
            'username': 'loginuser',
            'email': 'loginuser@example.com',
            'password': 'loginpass123'
        }
    )

    assert signup_response.status_code == 201

    login_response = client.post(
        '/login',
        json={
            'email': 'loginuser@example.com',
            'password': 'loginpass123'
        }
    )

    assert login_response.status_code == 200

    data = login_response.get_json()

    assert data['message'] == 'Login successful'
    assert 'token' in data
    assert data['username'] == 'loginuser'
    assert data['role'] == 'user'


# ---------------------------------------------------------
# Signup validation tests
# ---------------------------------------------------------

def test_signup_requires_request_body(client):
    response = client.post('/signup')

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Request body is required'


def test_signup_requires_all_fields(client):
    response = client.post(
        '/signup',
        json={
            'username': 'missingemail'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Username, email and password are required'


def test_signup_rejects_invalid_email(client):
    response = client.post(
        '/signup',
        json={
            'username': 'invalidemail',
            'email': 'invalid-email',
            'password': 'password123'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Invalid email format'


def test_signup_rejects_short_password(client):
    response = client.post(
        '/signup',
        json={
            'username': 'shortpassword',
            'email': 'shortpassword@example.com',
            'password': '1234567'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Password must be at least 8 characters'


def test_signup_rejects_short_username(client):
    response = client.post(
        '/signup',
        json={
            'username': 'ab',
            'email': 'shortusername@example.com',
            'password': 'password123'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Username must be between 3 and 50 characters'


def test_signup_rejects_duplicate_username(client):
    first_response = client.post(
        '/signup',
        json={
            'username': 'duplicateuser',
            'email': 'first@example.com',
            'password': 'password123'
        }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        '/signup',
        json={
            'username': 'duplicateuser',
            'email': 'second@example.com',
            'password': 'password123'
        }
    )

    assert second_response.status_code == 409

    data = second_response.get_json()

    assert data['error'] == 'Username already exists'


def test_signup_rejects_duplicate_email(client):
    first_response = client.post(
        '/signup',
        json={
            'username': 'firstemailuser',
            'email': 'duplicate@example.com',
            'password': 'password123'
        }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        '/signup',
        json={
            'username': 'secondemailuser',
            'email': 'duplicate@example.com',
            'password': 'password123'
        }
    )

    assert second_response.status_code == 409

    data = second_response.get_json()

    assert data['error'] == 'Email already exists'


# ---------------------------------------------------------
# Login validation tests
# ---------------------------------------------------------

def test_login_requires_request_body(client):
    response = client.post('/login')

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Request body is required'


def test_login_requires_email_and_password(client):
    response = client.post(
        '/login',
        json={
            'email': 'missingpassword@example.com'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Email and password are required'


def test_login_rejects_invalid_email(client):
    response = client.post(
        '/login',
        json={
            'email': 'invalid-email',
            'password': 'password123'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Invalid email format'


def test_login_rejects_short_password(client):
    response = client.post(
        '/login',
        json={
            'email': 'user@example.com',
            'password': '1234567'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Password must be at least 8 characters'


def test_login_rejects_wrong_password(client):
    signup_response = client.post(
        '/signup',
        json={
            'username': 'wrongpassworduser',
            'email': 'wrongpassword@example.com',
            'password': 'correctpass123'
        }
    )

    assert signup_response.status_code == 201

    login_response = client.post(
        '/login',
        json={
            'email': 'wrongpassword@example.com',
            'password': 'wrongpass123'
        }
    )

    assert login_response.status_code == 401

    data = login_response.get_json()

    assert data['error'] == 'Invalid email or password'


def test_disabled_user_cannot_login(client):
    from models import db, User
    from werkzeug.security import generate_password_hash

    user = User(
        username='disableduser',
        email='disabled@example.com',
        password_hash=generate_password_hash('password123'),
        role='user',
        is_active=False
    )

    db.session.add(user)
    db.session.commit()

    response = client.post(
        '/login',
        json={
            'email': 'disabled@example.com',
            'password': 'password123'
        }
    )

    assert response.status_code == 403

    data = response.get_json()

    assert data['error'] == 'Your account has been disabled'


# ---------------------------------------------------------
# JWT security tests
# ---------------------------------------------------------

def test_protected_route_requires_authorization_header(client):
    response = client.get('/tasks')

    assert response.status_code == 401

    data = response.get_json()

    assert data['error'] == 'Authorization token is required'


def test_protected_route_requires_bearer_token(client):
    response = client.get(
        '/tasks',
        headers={
            'Authorization': 'InvalidToken'
        }
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data['error'] == 'Authorization header must use Bearer token'


def test_protected_route_rejects_invalid_token(client):
    response = client.get(
        '/tasks',
        headers={
            'Authorization': 'Bearer invalid.jwt.token'
        }
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data['error'] == 'Invalid token'


def test_protected_route_rejects_expired_token(client):
    import jwt
    from datetime import datetime, timedelta

    from app import app

    expired_token = jwt.encode(
        {
            'user_id': 1,
            'role': 'user',
            'exp': datetime.utcnow() - timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    response = client.get(
        '/tasks',
        headers={
            'Authorization': f'Bearer {expired_token}'
        }
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data['error'] == 'Token expired'