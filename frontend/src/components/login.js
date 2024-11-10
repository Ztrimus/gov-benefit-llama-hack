import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function LoginPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        // Attempt to check if the user is already authenticated by calling /auth/check-profile
        const response = await axios.post(
          `${API_BASE_URL}/auth/check-profile`,{ email: sessionStorage.getItem('user_email') }, { withCredentials: true }
      );
        if (response.data.profileExists) {
          setIsAuthenticated(true);
          navigate('/dashboard');
        } else {
          setIsAuthenticated(true);
          navigate('/profile');
        }
      } catch (error) {
        console.error('User not authenticated:', error);
        setIsAuthenticated(false);
      }
    };

    checkAuthentication();
  }, [navigate]);

  const handleLoginSuccess = async (response) => {
    try {
      // Extract token from Google response
      const idToken = response.credential;
      console.log("ID Token:", idToken); // Debugging line

      // Send token to backend for verification and user creation
      const backendResponse = await axios.post(`${API_BASE_URL}/auth`, { token: idToken }, { withCredentials: true });
      
      console.log("Backend Response:", backendResponse.data); // Debugging line
      sessionStorage.setItem('user_name', backendResponse.data.user.name);
      sessionStorage.setItem('user_email', backendResponse.data.user.email);

      // After successful login, check profile status
      const profileResponse = await axios.get(`${API_BASE_URL}/auth/check-profile`, { withCredentials: true });

      if (profileResponse.data.profileExists) {
        setIsAuthenticated(true);
        navigate('/dashboard');
      } else {
        setIsAuthenticated(true);
        navigate('/profile');
      }
    } catch (error) {
      console.error('Error during backend authentication:', error);
    }
  };

  const handleLoginError = () => {
    console.log('Login Failed');
  };

  return (
    <GoogleOAuthProvider clientId='306243268653-mfufu71o6opbjqd3hdbknblpei9hmng3.apps.googleusercontent.com'>
      <div className="login-container">
        <div className="login-card">
          <h1>Welcome Back!</h1>
          <GoogleLogin
            onSuccess={handleLoginSuccess}
            onError={handleLoginError}
          />
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}

export default LoginPage;
