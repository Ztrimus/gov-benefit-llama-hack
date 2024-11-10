import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './UserProfile.css';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function UserProfile() {
  const [userInfo, setUserInfo] = useState({
    occupation: '',
    income: '',
    demographics: '',
    affiliated_organization: '',
    birthdate: '',
    email: sessionStorage.getItem('user_email')
  });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/auth/check-profile`,
          { email: sessionStorage.getItem('user_email') },
          { withCredentials: true }
        );
        
        // Only update userInfo if profile exists and response data includes the profile
        if (response.data.profileExists && response.data.profile) {
          setUserInfo((prevInfo) => ({
            ...prevInfo,
            ...response.data.profile
          }));
        }
      } catch (err) {
        console.error('Error fetching user profile:', err);
        setError('Failed to load user profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setUserInfo((prevInfo) => ({ ...prevInfo, [name]: value }));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccessMessage('');

    if (!userInfo.occupation || !userInfo.birthdate) {
      setError('Occupation and Birthdate are required.');
      setSubmitting(false);
      return;
    }

    try {
      await axios.post(`${API_BASE_URL}/update-profile`, userInfo, { withCredentials: true });
      setSuccessMessage('Profile updated successfully.');
      console.log('User profile updated successfully');
      navigate('/dashboard');
    } catch (err) {
      console.error('Error updating user profile:', err);
      setError('Failed to update profile.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="user-profile-container">
      <form onSubmit={handleSubmit} className="user-profile-form">
        <h1>User Information Page</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            {error && <p className="error-message">{error}</p>}
            <div className="form-group">
              <label htmlFor="occupation">Occupation:<span className="required">*</span></label>
              <input
                type="text"
                id="occupation"
                name="occupation"
                value={userInfo.occupation}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="income">Income:</label>
              <input
                type="number"
                id="income"
                name="income"
                value={userInfo.income}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="demographics">Demographics:</label>
              <input
                type="text"
                id="demographics"
                name="demographics"
                value={userInfo.demographics}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="affiliated_organization">Affiliated Organization:</label>
              <input
                type="text"
                id="affiliated_organization"
                name="affiliated_organization"
                value={userInfo.affiliated_organization}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="birthdate">Birthdate:<span className="required">*</span></label>
              <input
                type="date"
                id="birthdate"
                name="birthdate"
                value={userInfo.birthdate}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="submit-button" disabled={submitting}>
              {submitting ? 'Submitting...' : 'Submit'}
            </button>
            {successMessage && <p className="success-message">{successMessage}</p>}
          </>
        )}
      </form>
    </div>
  );
}

export default UserProfile;
