# EduVerse - Frontend
This directory contains the frontend for EduVerse, a modern Educational Resource Planning (ERP) system designed for colleges to manage student and faculty data. Built with React and styled with Tailwind CSS, this frontend provides a responsive and user-friendly interface, connecting to a Django backend API to handle data operations.
Features

Profile Page: Displays student details such as name, roll number, phone, address, and more, with an option to edit.
Edit Profile Page: Allows students to update their personal details (e.g., father’s name, mother’s name, admission date) and save changes to the backend.
Planned Features: Student login page, dashboard with attendance and fee insights, and integration of a chatbot and AI features for enhanced user interaction.
Styling: Fully responsive design using Tailwind CSS for a clean and modern look.

Setup Instructions
Prerequisites

Node.js 14+ (includes npm)
Backend API running at http://localhost:8000/api/ (see backend/README.md for setup)

Installation

Navigate to the Frontend Directory:
cd eduverse_project/frontend


Install Dependencies:
npm install


Configure API Base URL:

Open src/api/api.js and ensure the baseURL matches your backend API:const API = axios.create({
  baseURL: 'http://localhost:8000/api/students/',
  withCredentials: true,
});




Run the Development Server:
npm start


The app will be available at http://localhost:3000.



Project Structure
frontend/
├── public/
│   ├── index.html         # React entry point
│   └── images/            # Static images (e.g., default-profile.png)
├── src/
│   ├── assets/            # Assets (images, fonts)
│   │   └── images/
│   ├── components/        # Reusable React components
│   │   ├── Profile.js     # Component to display student profile
│   │   ├── EditProfile.js # Component for editing profile (WIP)
│   │   └── Navbar.js      # Navigation bar (planned)
│   ├── pages/             # Page-level components for routing
│   │   ├── ProfilePage.js # Profile page
│   │   ├── EditProfilePage.js # Edit profile page
│   │   ├── DashboardPage.js # Dashboard (planned)
│   │   └── LoginPage.js   # Login page (planned)
│   ├── api/               # API interaction logic
│   │   └── api.js         # Functions for API calls (e.g., fetchProfile)
│   ├── App.js             # Main app with routing
│   ├── index.js           # React entry point
│   ├── index.css          # Tailwind CSS setup
│   └── ...
├── tailwind.config.js     # Tailwind configuration
├── package.json           # Dependencies
└── README.md              # This file

Available Pages

/profile: View student profile details with an "Edit Profile" button.
/edit-profile: Edit student details and save changes to the backend (work in progress for full API integration).

Development Notes

Styling: Use Tailwind CSS classes for styling (e.g., bg-blue-500, p-4, text-center).
API Calls: Use axios in src/api/api.js to interact with the backend API.
Routing: Navigation is managed with react-router-dom in App.js.

Testing

Ensure the backend API is running (http://localhost:8000).
Visit http://localhost:3000/profile to view the profile page.
Test API connectivity by logging in via the backend and checking if profile data loads correctly.

Future Enhancements

Login Page: Add a form for student authentication.
Dashboard: Display attendance, fee status, and other insights.
Chatbot & AI: Integrate a chatbot for student queries and AI for predictive analytics (e.g., fee payment trends).
Visualizations: Use recharts for dashboard charts.

License
MIT License
