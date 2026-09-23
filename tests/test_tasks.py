from models import db, User, Task
from werkzeug.security import generate_password_hash


def create_user_and_get_token(client, username, email, password='password123'):
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role='user',
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    login_response = client.post(
        '/login',
        json={
            'email': email,
            'password': password
        }
    )

    assert login_response.status_code == 200

    return login_response.get_json()['token'], user


def test_create_task_success(client):
    token, user = create_user_and_get_token(
        client,
        'taskcreator',
        'taskcreator@example.com'
    )

    response = client.post(
        '/tasks',
        json={
            'title': 'Complete placement preparation',
            'description': 'Study DBMS and OS',
            'priority': 'High',
            'due_date': '2026-10-01'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data['message'] == 'Task created successfully'
    assert 'task_id' in data


def test_get_tasks_success(client):
    token, user = create_user_and_get_token(
        client,
        'taskgetter',
        'taskgetter@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Study SQL',
        description='Practice PostgreSQL',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    response = client.get(
        '/tasks',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['title'] == 'Study SQL'
    assert data[0]['priority'] == 'Medium'


def test_get_single_task_success(client):
    token, user = create_user_and_get_token(
        client,
        'singletaskuser',
        'singletask@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Single Task',
        description='Get this task',
        priority='Low'
    )

    db.session.add(task)
    db.session.commit()

    response = client.get(
        f'/tasks/{task.id}',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data['id'] == task.id
    assert data['title'] == 'Single Task'
    assert data['priority'] == 'Low'


def test_update_task_success(client):
    token, user = create_user_and_get_token(
        client,
        'taskupdater',
        'taskupdater@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Old Task',
        description='Old description',
        priority='Low'
    )

    db.session.add(task)
    db.session.commit()

    response = client.put(
        f'/tasks/{task.id}',
        json={
            'title': 'Updated Task',
            'description': 'Updated description',
            'completed': True,
            'priority': 'High',
            'due_date': '2026-12-31'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data['message'] == 'Task updated successfully'

    updated_task = db.session.get(Task, task.id)

    assert updated_task.title == 'Updated Task'
    assert updated_task.description == 'Updated description'
    assert updated_task.completed is True
    assert updated_task.priority == 'High'


def test_delete_task_success(client):
    token, user = create_user_and_get_token(
        client,
        'taskdeleter',
        'taskdeleter@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Delete Task',
        description='This task will be deleted',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    task_id = task.id

    response = client.delete(
        f'/tasks/{task_id}',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data['message'] == 'Task deleted successfully'

    deleted_task = db.session.get(Task, task_id)

    assert deleted_task is None


def test_user_cannot_access_another_users_task(client):
    token1, user1 = create_user_and_get_token(
        client,
        'owneruser',
        'owner@example.com'
    )

    token2, user2 = create_user_and_get_token(
        client,
        'otheruser',
        'other@example.com'
    )

    task = Task(
        user_id=user1.id,
        title='Private Task',
        description='Belongs to user 1',
        priority='High'
    )

    db.session.add(task)
    db.session.commit()

    response = client.get(
        f'/tasks/{task.id}',
        headers={
            'Authorization': f'Bearer {token2}'
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data['error'] == 'Task not found'


def test_user_cannot_update_another_users_task(client):
    token1, user1 = create_user_and_get_token(
        client,
        'updateowner',
        'updateowner@example.com'
    )

    token2, user2 = create_user_and_get_token(
        client,
        'updateother',
        'updateother@example.com'
    )

    task = Task(
        user_id=user1.id,
        title='Private Update Task',
        description='Belongs to user 1',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    response = client.put(
        f'/tasks/{task.id}',
        json={
            'title': 'Hacked Task'
        },
        headers={
            'Authorization': f'Bearer {token2}'
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data['error'] == 'Task not found'


def test_user_cannot_delete_another_users_task(client):
    token1, user1 = create_user_and_get_token(
        client,
        'deleteowner',
        'deleteowner@example.com'
    )

    token2, user2 = create_user_and_get_token(
        client,
        'deleteother',
        'deleteother@example.com'
    )

    task = Task(
        user_id=user1.id,
        title='Private Delete Task',
        description='Belongs to user 1',
        priority='Low'
    )

    db.session.add(task)
    db.session.commit()

    task_id = task.id

    response = client.delete(
        f'/tasks/{task_id}',
        headers={
            'Authorization': f'Bearer {token2}'
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data['error'] == 'Task not found'

    existing_task = db.session.get(Task, task_id)

    assert existing_task is not None


# ---------------------------------------------------------
# Create task validation tests
# ---------------------------------------------------------

def test_create_task_requires_request_body(client):
    token, user = create_user_and_get_token(
        client,
        'createmissingbody',
        'createmissingbody@example.com'
    )

    response = client.post(
        '/tasks',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Request body is required'


def test_create_task_requires_title(client):
    token, user = create_user_and_get_token(
        client,
        'notitleuser',
        'notitle@example.com'
    )

    response = client.post(
        '/tasks',
        json={
            'description': 'Task without title'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Task title is required'


def test_create_task_rejects_invalid_priority(client):
    token, user = create_user_and_get_token(
        client,
        'invalidpriority',
        'invalidpriority@example.com'
    )

    response = client.post(
        '/tasks',
        json={
            'title': 'Invalid Priority Task',
            'priority': 'Urgent'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Priority must be Low, Medium or High'


def test_create_task_rejects_invalid_due_date(client):
    token, user = create_user_and_get_token(
        client,
        'invalidduedate',
        'invalidduedate@example.com'
    )

    response = client.post(
        '/tasks',
        json={
            'title': 'Invalid Date Task',
            'due_date': '01-10-2026'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Due date must be in YYYY-MM-DD format'


def test_create_task_rejects_invalid_description_type(client):
    token, user = create_user_and_get_token(
        client,
        'invaliddescription',
        'invaliddescription@example.com'
    )

    response = client.post(
        '/tasks',
        json={
            'title': 'Invalid Description Task',
            'description': 12345
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Description must be a string'


# ---------------------------------------------------------
# Update task validation tests
# ---------------------------------------------------------

def test_update_task_rejects_invalid_completed_value(client):
    token, user = create_user_and_get_token(
        client,
        'invalidcompleted',
        'invalidcompleted@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Completed Validation Task',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    response = client.put(
        f'/tasks/{task.id}',
        json={
            'completed': 'true'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'completed must be true or false'


def test_update_task_rejects_invalid_priority(client):
    token, user = create_user_and_get_token(
        client,
        'updatepriority',
        'updatepriority@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Priority Validation Task',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    response = client.put(
        f'/tasks/{task.id}',
        json={
            'priority': 'Urgent'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Priority must be Low, Medium or High'


def test_update_task_rejects_invalid_due_date(client):
    token, user = create_user_and_get_token(
        client,
        'updateduedate',
        'updateduedate@example.com'
    )

    task = Task(
        user_id=user.id,
        title='Due Date Validation Task',
        priority='Medium'
    )

    db.session.add(task)
    db.session.commit()

    response = client.put(
        f'/tasks/{task.id}',
        json={
            'due_date': '2026/12/31'
        },
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Due date must be in YYYY-MM-DD format'


# ---------------------------------------------------------
# Task filtering validation tests
# ---------------------------------------------------------

def test_get_tasks_rejects_invalid_completed_filter(client):
    token, user = create_user_and_get_token(
        client,
        'invalidcompletedfilter',
        'invalidcompletedfilter@example.com'
    )

    response = client.get(
        '/tasks?completed=yes',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'completed must be true or false'


def test_get_tasks_rejects_invalid_priority_filter(client):
    token, user = create_user_and_get_token(
        client,
        'invalidpriorityfilter',
        'invalidpriorityfilter@example.com'
    )

    response = client.get(
        '/tasks?priority=Urgent',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data['error'] == 'Priority must be Low, Medium or High'