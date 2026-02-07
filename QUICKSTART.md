# Quick Start Guide

## Server Status
The Django development server should be running at: **http://127.0.0.1:8000/**

## First Steps

### 1. Create a Superuser (Admin Account)
Open a new terminal and run:
```bash
.\venv\Scripts\activate
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 2. Access the Application
- **Login/Register**: http://127.0.0.1:8000/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Dashboard**: http://127.0.0.1:8000/dashboard/ (after login)

### 3. Create Initial Categories (Optional)
After creating a superuser, you can add complaint categories:
1. Go to Admin Panel: http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Click on "Complaint Categories"
4. Add categories like:
   - Technical Issue
   - Service Complaint
   - Billing Issue
   - Facility Issue
   - etc.

Or use the Python shell:
```bash
python manage.py shell
```
Then run the code from `setup_initial_data.py`

## Default Database
The application is currently using **SQLite** (db.sqlite3) for easy setup.
To switch to MySQL, update the `.env` file with:
```
DB_ENGINE=mysql
DB_NAME=complaints_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

## Features Available
- ✅ User Registration & Login
- ✅ Create Complaints
- ✅ View All Complaints
- ✅ Filter & Search Complaints
- ✅ Update Complaint Status (Staff)
- ✅ Add Comments
- ✅ View Complaint History
- ✅ Dashboard with Statistics
- ✅ File Attachments

## Troubleshooting

If the server is not running, start it with:
```bash
.\venv\Scripts\activate
python manage.py runserver
```

To stop the server, press `Ctrl+C` in the terminal where it's running.
