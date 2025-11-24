# Part 3: Web Application - Caregivers Platform

## Overview

This is a Flask web application that provides full CRUD (Create, Read, Update, Delete) operations for all database tables in the Caregivers Platform.

## Features

- **Complete CRUD Operations** for all tables:
  - Users
  - Caregivers
  - Members
  - Jobs
  - Job Applications
  - Appointments

- **Modern UI** with responsive design
- **Flash messages** for user feedback
- **Form validation** on both client and server side
- **Relationship handling** (e.g., creating a caregiver automatically creates a user)

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Make sure PostgreSQL is running** and the database `caregivers_db` exists.

3. **Run the application:**
```bash
python app.py
```

4. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`

## Project Structure

```
backend/
├── app.py                 # Flask application with all routes
├── models.py              # Database models (shared with Part 2)
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── users/            # User CRUD templates
│   ├── caregivers/       # Caregiver CRUD templates
│   ├── members/          # Member CRUD templates
│   ├── jobs/             # Job CRUD templates
│   ├── job_applications/ # Job Application CRUD templates
│   └── appointments/     # Appointment CRUD templates
└── static/
    └── css/
        └── style.css     # Modern CSS styling
```

## Routes

### Users
- `GET /users` - List all users
- `GET /users/create` - Create user form
- `POST /users/create` - Create user
- `GET /users/<id>/edit` - Edit user form
- `POST /users/<id>/edit` - Update user
- `POST /users/<id>/delete` - Delete user

### Caregivers
- `GET /caregivers` - List all caregivers
- `GET /caregivers/create` - Create caregiver form
- `POST /caregivers/create` - Create caregiver (creates user automatically)
- `GET /caregivers/<id>/edit` - Edit caregiver form
- `POST /caregivers/<id>/edit` - Update caregiver
- `POST /caregivers/<id>/delete` - Delete caregiver

### Members
- `GET /members` - List all members
- `GET /members/create` - Create member form
- `POST /members/create` - Create member (creates user and address automatically)
- `GET /members/<id>/edit` - Edit member form
- `POST /members/<id>/edit` - Update member
- `POST /members/<id>/delete` - Delete member

### Jobs
- `GET /jobs` - List all jobs
- `GET /jobs/create` - Create job form
- `POST /jobs/create` - Create job
- `GET /jobs/<id>/edit` - Edit job form
- `POST /jobs/<id>/edit` - Update job
- `POST /jobs/<id>/delete` - Delete job

### Job Applications
- `GET /job_applications` - List all job applications
- `GET /job_applications/create` - Create job application form
- `POST /job_applications/create` - Create job application
- `POST /job_applications/<caregiver_id>/<job_id>/delete` - Delete job application

### Appointments
- `GET /appointments` - List all appointments
- `GET /appointments/create` - Create appointment form
- `POST /appointments/create` - Create appointment
- `GET /appointments/<id>/edit` - Edit appointment form
- `POST /appointments/<id>/edit` - Update appointment
- `POST /appointments/<id>/delete` - Delete appointment

## Deployment

### For Local Development
The app runs on `http://localhost:5000` by default.

### For Production Deployment

#### Option 1: PythonAnywhere (Free)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code
3. Configure the web app to use your Flask app
4. Set up the database connection
5. Update the database URL in `models.py` if needed

#### Option 2: Heroku
1. Install Heroku CLI
2. Create a `Procfile`:
```
web: gunicorn app:app
```
3. Deploy:
```bash
heroku create
git push heroku main
```

#### Option 3: AWS Educational Tier
1. Use your `@nu.edu.kz` email to access AWS Educate
2. Launch an EC2 instance
3. Install Python, PostgreSQL, and dependencies
4. Run the Flask app with a production WSGI server (gunicorn)

## Notes

- The application uses the same database models as Part 2
- All database operations use SQLAlchemy ORM
- Flash messages provide user feedback for all operations
- Forms include validation for required fields
- The UI is responsive and works on mobile devices

## Troubleshooting

- **Database connection errors**: Make sure PostgreSQL is running and the database exists
- **Import errors**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
- **Port already in use**: Change the port in `app.py` (last line)

