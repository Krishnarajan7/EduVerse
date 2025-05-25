import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';
import EditProfilePage from './pages/EditProfilePage';
import LoginPage from './pages/LoginPage';
import { useEffect, useState } from 'react';
import { fetchProfile, setAuthToken } from './api';

function App() {
  const [role, setRole] = useState(null);

  useEffect(() => {
    const checkUserRole = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        setAuthToken(token);
        try {
          const response = await fetchProfile();
          setRole('student'); // Adjust based on API response
        } catch (error) {
          setRole(null);
          setAuthToken(null);
          localStorage.removeItem('token');
        }
      }
    };
    checkUserRole();
  }, []);

  return (
    <Router>
      <nav className="bg-gray-800 text-white p-4">
        <Link to="/" className="mr-4">Home</Link>
        {role === 'student' && (
          <>
            <Link to="/profile" className="mr-4">Profile</Link>
            <Link to="/edit-profile" className="mr-4">Edit Profile</Link>
            <Link to="/exam" className="mr-4">Exam</Link>
            <Link to="/transport" className="mr-4">Transport</Link>
          </>
        )}
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/" element={<div className="p-4">Welcome to EduVerse</div>} />
        <Route path="/profile" element={role === 'student' ? <ProfilePage /> : <Navigate to="/login" />} />
        <Route path="/edit-profile" element={role === 'student' ? <EditProfilePage /> : <Navigate to="/login" />} />
        <Route path="/exam" element={role === 'student' ? <div className="p-4">Exam Page (To be implemented)</div> : <Navigate to="/login" />} />
        <Route path="/transport" element={role === 'student' ? <div className="p-4">Transport Page (To be implemented)</div> : <Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Router>
  );
}

export default App;