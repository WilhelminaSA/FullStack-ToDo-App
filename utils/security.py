from datetime import datetime, timedelta
from functools import wraps
import re

import jwt
from flask import current_app, request, jsonify

from models import db, User


def is_valid_email(email):
    email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return re.match(email_pattern, email) is not None


def generate_token(user):
    payload = {
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'error': 'Authorization token is required'
            }), 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'error': 'Authorization header must use Bearer token'
            }), 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )

            user_id = payload.get('user_id')

            if not user_id:
                return jsonify({
                    'error': 'Invalid token'
                }), 401

            user = db.session.get(User, user_id)

            if not user:
                return jsonify({
                    'error': 'User not found'
                }), 401

            if not user.is_active:
                return jsonify({
                    'error': 'Your account has been disabled'
                }), 403

        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token expired'
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                'error': 'Invalid token'
            }), 401

        return f(user, *args, **kwargs)

    return decorated


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'error': 'Authorization token is required'
            }), 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'error': 'Authorization header must use Bearer token'
            }), 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )

            user_id = payload.get('user_id')

            if not user_id:
                return jsonify({
                    'error': 'Invalid token'
                }), 401

            user = db.session.get(User, user_id)

            if not user:
                return jsonify({
                    'error': 'User not found'
                }), 401

            if not user.is_active:
                return jsonify({
                    'error': 'Admin account is disabled'
                }), 403

            if user.role != 'admin':
                return jsonify({
                    'error': 'Admin access required'
                }), 403

        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token expired'
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                'error': 'Invalid token'
            }), 401

        return f(user, *args, **kwargs)

    return decorated