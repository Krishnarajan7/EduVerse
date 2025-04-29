import { useState, useEffect } from 'react';
import { fetchProfile } from '../api/api';

function ProfilePage() {
  const [student, setStudent] = useState(null);

  useEffect(() => {
    fetchProfile()
      .then(response => setStudent(response.data))
      .catch(error => console.error('Error fetching profile:', error));
  }, []);

  if (!student) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Profile Page</h1>
      <div className="mt-4">
        <p><strong>Name:</strong> {student.name}</p>
        <p><strong>Roll Number:</strong> {student.roll_number}</p>
        <p><strong>Phone:</strong> {student.phone}</p>
        <p><strong>Address:</strong> {student.address}</p>
      </div>
    </div>
  );
}

export default ProfilePage;