EduVerse - Educational ERP System
Overview
EduVerse is a modern Educational Resource Planning (ERP) system designed to manage student data efficiently. It features a Django REST Framework (DRF) backend for API-driven data management and a React frontend (built with Vite) for a responsive user interface. Key features include student profile management, edit profile functionality, and navigation between pages like /profile and /edit-profile.
Tech Stack

Backend: Django, Django REST Framework, SQLite
Frontend: React, Vite, Tailwind CSS, React Router, Axios
Authentication: Session-based (Django), JWT planned for future
Deployment: Localhost (future: Docker, AWS)

Project Structure
eduverse_project/
├── backend/
│   ├── eduverse_project/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── students/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── .venv/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── vite.svg
│   │   └── images/
│   │       └── default-profile.png
│   ├── src/
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── Profile.jsx
│   │   │   ├── EditProfile.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   ├── ProfilePage.jsx
│   │   │   ├── EditProfilePage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   └── LoginPage.jsx
│   │   ├── api/
│   │   │   └── api.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── vite-env.d.ts
│   ├── .gitignore
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md

Prerequisites

Python (3.8+)
Node.js (v22.9.0+)
npm (11.3.0+)
Git

Setup Instructions
Backend Setup

Navigate to the backend directory:cd eduverse_project/backend


Create and activate a virtual environment:python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


Install dependencies:pip install -r requirements.txt

If requirements.txt is missing, install these:pip install django djangorestframework


Run migrations:python manage.py migrate


Create a superuser (admin):python manage.py createsuperuser


Start the backend server:python manage.py runserver


Access the API at http://localhost:8000/api/students/.
Admin panel: http://localhost:8000/admin/.



Frontend Setup

Navigate to the frontend directory:cd eduverse_project/frontend


Install dependencies:npm install

Ensure these are installed:
react, react-dom, react-router-dom, axios
Dev: vite, tailwindcss, @tailwindcss/postcss, postcss, autoprefixer


Start the frontend server:npm run dev


Access the app at http://localhost:5173.



Usage

Backend:
Log in via /api/students/login/ (e.g., username: 1a001, password: Student@123).
Test endpoints like /api/students/profile/ to fetch student data.


Frontend:
Visit http://localhost:5173/profile to view student details.
Navigate to http://localhost:5173/edit-profile to edit student info.
Ensure the backend is running for API calls.



API Endpoints

GET /api/students/profile/: Fetch student profile.
POST /api/students/profile/: Update student profile.
GET /api/students/dashboard/: Fetch dashboard data (fees, circulars, etc.).
POST /api/students/login/: Authenticate student.
POST /api/students/logout/: Log out.

Features

Profile Management: View and edit student details (name, phone, address).
Navigation: React Router for seamless page transitions.
Styling: Tailwind CSS for responsive design.
API Integration: Axios for backend communication.

Future Enhancements

Add login page on the frontend.
Implement JWT authentication.
Expand features (attendance, fees, timetable).
Deploy with Docker and AWS.

Contributing

Fork the repository.
Create a branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your message".
Push to branch: git push origin feature/your-feature.
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
