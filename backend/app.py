from datetime import datetime
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

from models import db, User, Task
from routes.auth import auth_bp
from utils.security import (
    generate_token,
    token_required,
    admin_required,
    is_valid_email
)


load_dotenv()


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:5173"
        }
    }
)


database_url = os.getenv(
    'DATABASE_URL',
    'sqlite:///todo.db'
)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


secret_key = os.getenv('SECRET_KEY')

if not secret_key:
    raise RuntimeError('SECRET_KEY is not set')


app.config['SECRET_KEY'] = secret_key


db.init_app(app)


app.register_blueprint(auth_bp)


with app.app_context():
    db.create_all()


def is_valid_priority(priority):
    return priority in ['Low', 'Medium', 'High']


def is_valid_role(role):
    return role in ['user', 'admin']


def parse_due_date(due_date):
    """
    Validate and convert a due date in YYYY-MM-DD format.
    """

    if not isinstance(due_date, str):
        return None

    try:
        return datetime.strptime(
            due_date,
            '%Y-%m-%d'
        )
    except ValueError:
        return None


def task_to_dict(task):
    return {
        'id': task.id,
        'user_id': task.user_id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'completed': task.completed,
        'due_date': (
            task.due_date.isoformat()
            if task.due_date
            else None
        ),
        'created_at': (
            task.created_at.isoformat()
            if task.created_at
            else None
        )
    }


def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': (
            user.created_at.isoformat()
            if user.created_at
            else None
        )
    }


@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to the To-Do List API'
    }), 200


# ============================================================
# TASK ROUTES
# ============================================================

@app.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'error': 'Request body is required'
        }), 400

    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    due_date = data.get('due_date')

    if not title:
        return jsonify({
            'error': 'Task title is required'
        }), 400

    if not isinstance(title, str):
        return jsonify({
            'error': 'Title must be a string'
        }), 400

    if len(title) > 100:
        return jsonify({
            'error': 'Title must not exceed 100 characters'
        }), 400

    if description is not None and not isinstance(description, str):
        return jsonify({
            'error': 'Description must be a string'
        }), 400

    if not is_valid_priority(priority):
        return jsonify({
            'error': 'Priority must be Low, Medium or High'
        }), 400

    parsed_due_date = None

    if due_date is not None:

        parsed_due_date = parse_due_date(due_date)

        if parsed_due_date is None:
            return jsonify({
                'error': 'Due date must be in YYYY-MM-DD format'
            }), 400

    task = Task(
        user_id=current_user.id,
        title=title,
        description=description,
        priority=priority,
        due_date=parsed_due_date,
        completed=False
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        'message': 'Task created successfully',
        'task_id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'completed': task.completed,
        'due_date': (
            task.due_date.isoformat()
            if task.due_date
            else None
        ),
        'created_at': (
            task.created_at.isoformat()
            if task.created_at
            else None
        )
    }), 201


@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):

    completed = request.args.get('completed')
    priority = request.args.get('priority')

    query = Task.query.filter_by(
        user_id=current_user.id
    )

    if completed is not None:

        if completed.lower() not in ['true', 'false']:
            return jsonify({
                'error': 'completed must be true or false'
            }), 400

        completed_value = completed.lower() == 'true'

        query = query.filter_by(
            completed=completed_value
        )

    if priority is not None:

        if not is_valid_priority(priority):
            return jsonify({
                'error': 'Priority must be Low, Medium or High'
            }), 400

        query = query.filter_by(
            priority=priority
        )

    tasks = query.order_by(
        Task.id
    ).all()

    return jsonify([
        task_to_dict(task)
        for task in tasks
    ]), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):

    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            'error': 'Task not found'
        }), 404

    if task.user_id != current_user.id:
        return jsonify({
            'error': 'Task not found'
        }), 404

    return jsonify(
        task_to_dict(task)
    ), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):

    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            'error': 'Task not found'
        }), 404

    if task.user_id != current_user.id:
        return jsonify({
            'error': 'Task not found'
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'error': 'Request body is required'
        }), 400

    if 'title' in data:

        if not isinstance(data['title'], str):
            return jsonify({
                'error': 'Title must be a string'
            }), 400

        if not data['title']:
            return jsonify({
                'error': 'Task title is required'
            }), 400

        if len(data['title']) > 100:
            return jsonify({
                'error': 'Title must not exceed 100 characters'
            }), 400

        task.title = data['title']

    if 'description' in data:

        if data['description'] is not None and not isinstance(
            data['description'],
            str
        ):
            return jsonify({
                'error': 'Description must be a string'
            }), 400

        task.description = data['description']

    if 'priority' in data:

        if not is_valid_priority(data['priority']):
            return jsonify({
                'error': 'Priority must be Low, Medium or High'
            }), 400

        task.priority = data['priority']

    if 'completed' in data:

        if not isinstance(data['completed'], bool):
            return jsonify({
                'error': 'completed must be true or false'
            }), 400

        task.completed = data['completed']

    if 'due_date' in data:

        if data['due_date'] is None:
            task.due_date = None

        else:

            parsed_due_date = parse_due_date(
                data['due_date']
            )

            if parsed_due_date is None:
                return jsonify({
                    'error': 'Due date must be in YYYY-MM-DD format'
                }), 400

            task.due_date = parsed_due_date

    db.session.commit()

    return jsonify({
        'message': 'Task updated successfully',
        'task': task_to_dict(task)
    }), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):

    task = db.session.get(Task, task_id)

    if not task:
        return jsonify({
            'error': 'Task not found'
        }), 404

    if task.user_id != current_user.id:
        return jsonify({
            'error': 'Task not found'
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        'message': 'Task deleted successfully'
    }), 200


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route('/admin/login', methods=['POST'])
def admin_login():

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
            'error': 'Admin account is disabled'
        }), 403

    if user.role != 'admin':
        return jsonify({
            'error': 'Admin access required'
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
        'message': 'Admin login successful',
        'token': token,
        'admin_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200


# ============================================================
# ADMIN USER MANAGEMENT
# ============================================================

@app.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users(current_admin):

    users = User.query.order_by(
        User.id
    ).all()

    return jsonify([
        user_to_dict(user)
        for user in users
    ]), 200


@app.route('/admin/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(current_admin, user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'error': 'Request body is required'
        }), 400

    if 'username' in data:

        username = data['username']

        if not isinstance(username, str) or len(username) < 3 or len(username) > 50:
            return jsonify({
                'error': 'Username must be between 3 and 50 characters'
            }), 400

        existing_user = User.query.filter(
            User.username == username,
            User.id != user.id
        ).first()

        if existing_user:
            return jsonify({
                'error': 'Username already exists'
            }), 409

        user.username = username

    if 'email' in data:

        email = data['email']

        if not isinstance(email, str) or not is_valid_email(email):
            return jsonify({
                'error': 'Invalid email format'
            }), 400

        existing_user = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing_user:
            return jsonify({
                'error': 'Email already exists'
            }), 409

        user.email = email

    if 'role' in data:

        if not is_valid_role(data['role']):
            return jsonify({
                'error': 'Role must be user or admin'
            }), 400

        user.role = data['role']

    if 'is_active' in data:

        if not isinstance(data['is_active'], bool):
            return jsonify({
                'error': 'is_active must be true or false'
            }), 400

        user.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': user_to_dict(user)
    }), 200


@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_admin, user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404

    if user.id == current_admin.id:
        return jsonify({
            'error': 'Admin cannot delete their own account'
        }), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message': 'User deleted successfully'
    }), 200


# ============================================================
# ADMIN TASK MANAGEMENT
# ============================================================

@app.route('/admin/tasks', methods=['GET'])
@admin_required
def get_all_tasks(current_admin):

    tasks = Task.query.order_by(
        Task.id
    ).all()

    return jsonify([
        task_to_dict(task)
        for task in tasks
    ]), 200


if __name__ == '__main__':
    app.run(debug=True)