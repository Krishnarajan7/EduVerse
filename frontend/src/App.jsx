import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';
import EditProfilePage from './pages/EditProfilePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>Home</div>} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/edit-profile" element={<EditProfilePage />} />
      </Routes>
    </Router>
  );
}

export default App;