# EduVerse - Backend

This directory contains the backend for EduVerse, built with Django and Django REST Framework. It serves as an API to manage student and faculty data, providing endpoints for features like profile management, authentication, and password resets.

## Features
- **API Endpoints**:
  - `/api/students/profile/`: View and update student profiles.
  - `/api/students/login/`: Authenticate students.
  - `/api/students/logout/`: Log out users.
  - `/api/students/forgot-password/`: Request password reset link.
  - `/api/students/reset-password/<token>/`: Reset password using a token.
- **Database Models**:
  - `Student`: Stores student data (name, roll number, profile picture, etc.).
  - `Fee`, `Attendance`, etc.: Related models for student management.
- **Security**: Session-based authentication, secure password reset with token expiry.

## Setup Instructions
### Prerequisites
- Python 3.8+
- PostgreSQL (configured in `settings.py`)
- Virtual environment (recommended)

### Installation
1. **Clone the Repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd eduverse/backend