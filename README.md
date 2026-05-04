# Task Tracking Manager API

## Overview

Task Tracking Manager API is a Django REST Framework project for creating, assigning, and tracking tasks between users.

The project focuses on user-specific data access, object-level permissions, and field-level update restrictions. It is built as a practice backend API project to improve Django, DRF, authentication, permissions, and REST API design skills.

## Features

- Create, view, update, and delete tasks
- Assign tasks to other users
- Track task status
- Store due dates and completion timestamps
- Automatically set task owner on creation
- Restrict task visibility based on owner and assignee
- Restrict assignee updates to the task status field only

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite for local development
- PostgreSQL planned
- Git / GitHub

## Access Control

### Owner

The task owner can:

- view the task
- update task fields
- assign or change the assignee
- delete the task

### Assignee

The assigned user can:

- view the assigned task
- update only the task status

The assigned user cannot:

- edit title
- edit description
- edit due date
- change assignee
- delete the task

### Other users

Other authenticated users:

- cannot see the task
- receive `404 Not Found` responses

## API Endpoints

Current task endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | List available tasks |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/{id}/` | Retrieve a task |
| PATCH | `/api/tasks/{id}/` | Partially update a task |
| PUT | `/api/tasks/{id}/` | Fully update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

Authentication endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api-auth/login/` | Log in using DRF browsable API |
| POST | `/api-auth/logout/` | Log out |

## Local Setup

Clone the repository:

```bash
git clone https://github.com/ma1z0/Task-Tracking-Manager.git
cd Task-Tracking-Manager/TTM
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the API in the browser:

```text
http://127.0.0.1:8000/api/tasks/
```

## Current Status

Implemented:
- Task model
- Task serializer
- Task ViewSet
- DRF router-based endpoints
- Owner and assignee relations
- Authenticated-only API access
- Queryset filtering by owner or assignee
- Custom object-level permissions
- Field-level validation for assignee updates

## Roadmap

Planned improvements:
- Add task filtering by status
- Add search by title and description
- Add ordering by due date and creation date
- Add PostgreSQL support
- Add Docker Compose setup
- Add environment variables
- Add automated tests
- Add JWT authentication
