from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User
from utils.security import generate_token, is_valid_email


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'error': 'Request body is required'
        }), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({
            'error': 'Username, email and password are required'
        }), 400

    if not isinstance(username, str) or len(username) < 3 or len(username) > 50:
        return jsonify({
            'error': 'Username must be between 3 and 50 characters'
        }), 400

    if not isinstance(email, str) or not is_valid_email(email):
        return jsonify({
            'error': 'Invalid email format'
        }), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({
            'error': 'Password must be at least 8 characters'
        }), 400

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return jsonify({
            'error': 'Username already exists'
        }), 409

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            'error': 'Email already exists'
        }), 409

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role='user',
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'error': 'Request body is required'
        }), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            'error': 'Email and password are required'
        }), 400

    if not isinstance(email, str) or not is_valid_email(email):
        return jsonify({
            'error': 'Invalid email format'
        }), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({
            'error': 'Password must be at least 8 characters'
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            'error': 'Invalid email or password'
        }), 401

    if not user.is_active:
        return jsonify({
            'error': 'Your account has been disabled'
        }), 403

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({
            'error': 'Invalid email or password'
        }), 401

    token = generate_token(user)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200