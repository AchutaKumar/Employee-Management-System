# Employee Management System

A straightforward Employee Management System built with **Django** and **MySQL**. This application provides an easy-to-use interface to manage employee records, including their details, department, and salary information.

## Features

- **User Authentication:** Secure login and logout functionality to protect employee records.
- **CRUD Operations:** Create, Read, Update, and Delete employee profiles.
- **Search Functionality:** Easily search for employees by their name or department.
- **Employee Details:** Stores comprehensive employee information:
  - Name
  - Email (Unique)
  - Department
  - Salary
  - Joining Date

## Tech Stack

- **Backend:** Python, Django
- **Database:** MySQL
- **Frontend:** HTML, CSS (Django Templates)

## Prerequisites

Before running this project, ensure you have the following installed:
- Python (3.x recommended)
- MySQL Server
- `pip` (Python package manager)

## Setup and Installation

Follow these steps to set up the project locally:

1. **Clone the repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd "Employee Management System"
   ```

2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Since this project uses MySQL, you will need the MySQL database connector. Install Django and the mysqlclient:
   ```bash
   pip install django mysqlclient
   ```

4. **Database Configuration:**
   - Ensure your MySQL server is running.
   - Create a new MySQL database named `employee_management_sys`:
     ```sql
     CREATE DATABASE employee_management_sys;
     ```
   - If your MySQL username or password is not `root` and `loyalsam` respectively, update the `DATABASES` configuration in `backend/settings.py` to match your local MySQL setup.

5. **Run Migrations:**
   Apply the database migrations to create the necessary tables.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up your username, email, and password.

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application:**
   Open your web browser and go to `http://127.0.0.1:8000/`. You will be redirected to the login page where you can log in using the superuser account you just created.

## Project Structure

```text
Employee Management System/
│
├── backend/                   # Main Django Project Directory
│   ├── settings.py            # Global project settings (database, installed apps)
│   ├── urls.py                # Main URL routing configuration
│   ├── asgi.py                # ASGI config for async web servers
│   └── wsgi.py                # WSGI config for web servers
│
├── employees/                 # Core Employee Management App
│   ├── migrations/            # Database schema migrations
│   ├── static/                # Static assets (CSS, JavaScript, Images)
│   ├── templates/             # HTML templates for views
│   ├── admin.py               # Django admin portal configurations
│   ├── forms.py               # Django forms for user inputs and validation
│   ├── models.py              # Database models (Employee schema)
│   ├── urls.py                # App-specific URL routes
│   └── views.py               # Business logic and controller functions
│
├── manage.py                  # Django's command-line utility
└── README.md                  # Project documentation
```

## Future Enhancements

Potential features that could be added in future iterations:
- **Role-Based Access Control (RBAC):** Allow different permissions for Admin and Standard Users (e.g., HR team vs regular employees).
- **Pagination:** Implement pagination on the employee list for better performance with large datasets.
- **Export Functionality:** Export the employee list to CSV or PDF formats.
- **Profile Pictures:** Ability to upload and display employee avatars.

## Contributing

Contributions are welcome! If you'd like to improve the project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE).
