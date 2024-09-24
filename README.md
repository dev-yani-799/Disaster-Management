Disaster Management System

Overview
This project is a web-based Disaster Management System built using Python and Django. It aims to streamline the management of disaster-related data and provide quick, accurate information to the relevant authorities and the public.
The system helps in managing data related to disasters, response teams, victims, and provides real-time alerts for quicker response in emergencies.

Features
User Authentication: Login and registration for authorized users.
Disaster Reports: Users can submit and view approve status.
Real-Time Alerts: Sends alerts based on recent disaster to admin and statecommitees.
GIS Integration: Displays disaster-prone areas on maps.

Technologies Used
Backend: Python, Django
Frontend: HTML, CSS, JavaScript, Bootstrap
Database: SQLite 
APIs : Google Maps API for GIS integration

Step 1: Install dependencies
pip install -r requirements.txt

Step 2: Migrate the database
python manage.py makemigrations
python manage.py migrate

Step 3: Run the development server
python manage.py runserver


Now, open your browser and go to http://127.0.0.1:8000/ to view the project.
