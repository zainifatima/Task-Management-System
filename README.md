# Task Management System (Django)

A task management web application built using Django. Admin task assign to the department team.

## Features
- User Authentication (Login/Signup)
- Create Tasks
- Assign task to the team
- Update & Delete Tasks
- Dashboard View

## Tech Stack
- Django
- Python
- SQLite / PostgreSQL
- HTML, CSS, Bootstrap

## Setup Instructions

```bash
git clone https://github.com/zainifatima/task-management-system.git
cd taskproject
python -m venv taskenv
taskenv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver