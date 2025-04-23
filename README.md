# EduVerse 

EduVerse is an Educational Resource Planning (ERP) system designed for colleges to manage student and faculty data efficiently. Built for a final year project, it supports up to 10,000 students with features like profile management, attendance tracking, fee management, and secure password resets. The system is transitioning to a modern UI with React and Tailwind CSS, backed by a Django API, and plans to integrate a chatbot and AI features for enhanced functionality.

## Project Structure
eduverse/
├── backend/        # Django backend (API)
│   ├── manage.py
│   └── README.md   # Backend-specific documentation
├── frontend/       # React frontend
│   └── README.md   # Frontend-specific documentation
└── README.md       # Project overview (this file)


## Features
- **Student Management**: Profile viewing/editing, attendance tracking, fee management.
- **Security**: Email-based password reset with token expiry.
- **Planned Features**: Chatbot for student queries, AI for predictive analytics (e.g., fee payment trends).

## Getting Started
1. **Backend Setup**: Follow instructions in `backend/README.md` to set up the Django API.
2. **Frontend Setup**: Follow instructions in `frontend/README.md` to set up the React app.
3. **Run the Project**:
   - Start the backend: `cd backend && python manage.py runserver`
   - Start the frontend: `cd frontend && npm start`
   - Access the app at `http://localhost:3000/profile`.

## Tech Stack
- **Backend**: Django, Python, Django REST Framework, MySQL/PostgreSQL
- **Frontend**: React, Tailwind CSS, JavaScript
- **Utilities**: UUID (tokens), SMTP (email), Git (version control)

## Contributing
This is a final year project, but feel free to fork and submit pull requests if you’d like to contribute!

## License
MIT License