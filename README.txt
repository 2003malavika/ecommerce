PRODUCT MANAGEMENT SYSTEM

Technology:
Python
Django
HTML
CSS
Bootstrap
SQLite

HOW TO RUN

1. Open the project folder in VS Code.

2. Open the terminal.

3. Create a virtual environment:

python -m venv env

4. Activate it on Windows:

env\Scripts\activate

5. Install Django:

pip install -r requirements.txt

6. Create the database:

python manage.py makemigrations
python manage.py migrate

7. Create an admin/login user:

python manage.py createsuperuser

Enter your username, email and password.

8. Start the server:

python manage.py runserver

9. Open this in your browser:

http://127.0.0.1:8000/

LOGIN

Use the username and password created with createsuperuser.

PROJECT FLOW

Browser
↓
URL
↓
View
↓
Model / Form
↓
SQLite Database
↓
Template
↓
Browser

IMPORTANT

This project is intentionally simple and beginner friendly.
The project uses Django's built-in authentication.
Only logged-in users can manage products.
