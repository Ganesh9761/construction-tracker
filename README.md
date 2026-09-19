# Construction Project Cost & Progress Tracker

This project is a web application for managing construction project costs and progress.

It allows project users to manage projects, construction phases, expenses and progress updates from one place.

## Features

- User login and role-based access
- Create and manage construction projects
- Add and manage project phases
- Record construction expenses
- Track phase completion
- View project budget and actual expenses
- View remaining budget and budget utilization
- Phase-wise financial analysis
- Construction cost escalation chart
- Project progress dashboard
- Audit logs
- User management

## Roles

The application currently supports:

- Admin
- Project Manager
- Site Engineer

Different roles have different permissions.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js
- pytest

## Project Structure

```text
construction-tracker/
├── app/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
├── migrations/
├── tests/
├── config.py
├── run.py
├── requirements.txt
└── README.md
