import { useState, useEffect } from 'react';
import { fetchProfile, updateProfile } from '../api/api';

function EditProfilePage() {
  const [formData, setFormData] = useState({ name: '', phone: '', address: '' });

  useEffect(() => {
    fetchProfile()
      .then(response => setFormData(response.data))
      .catch(error => console.error('Error fetching profile:', error));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    updateProfile(formData)
      .then(() => alert('Profile updated!'))
      .catch(error => console.error('Error updating profile:', error));
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Edit Profile</h1>
      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div>
          <label className="block">Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>
        <div>
          <label className="block">Phone:</label>
          <input
            type="text"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>
        <div>
          <label className="block">Address:</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Save Changes
        </button>
      </form>
    </div>
  );
}

export default EditProfilePage;