import React, { useEffect, useState } from 'react';
import './Dashboard.css';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function Dashboard() {
  const [matchedGrants, setMatchedGrants] = useState([]);
  const [appliedGrants, setAppliedGrants] = useState([]);
  const [error, setError] = useState(null);

  // Function to fetch matched grants from the API
  const fetchMatchedGrants = async () => {
    setError(null);  // Reset error state before fetching
    try {
      const response = await fetch(`${API_BASE_URL}/grants`, {
        credentials: 'include',  // Needed for session-based authentication
      });
      if (response.status === 401) {
        console.error('User is not authenticated');
        setError('You need to log in to access grants.');
        // Optionally, you can redirect to a login page here
      } else if (response.ok) {
        const grants = await response.json();
        setMatchedGrants(grants);
      } else {
        console.error('Failed to fetch grants');
        setError('Failed to load matched grants. Please try again later.');
      }
    } catch (error) {
      console.error('Error fetching grants:', error);
      setError('An error occurred while loading matched grants.');
    }
  };

  // Function to fetch applied grants status from the API
  const fetchAppliedGrants = async () => {
    setError(null);  // Reset error state before fetching
    try {
      const response = await fetch(`${API_BASE_URL}/applied-grants`, {
        credentials: 'include',
      });
      if (response.status === 401) {
        console.error('User is not authenticated');
        setError('You need to log in to access applied grants status.');
        // Optionally, you can redirect to a login page here
      } else if (response.ok) {
        const appliedGrantsData = await response.json();
        setAppliedGrants(appliedGrantsData);
      } else {
        console.error('Failed to fetch applied grants');
        setError('Failed to load applied grants status. Please try again later.');
      }
    } catch (error) {
      console.error('Error fetching applied grants:', error);
      setError('An error occurred while loading applied grants status.');
    }
  };

  // Fetch matched grants and applied grants on component mount
  useEffect(() => {
    fetchMatchedGrants();
    fetchAppliedGrants();
  }, []);

  return (
    <div className="dashboard-container">
      {error && <p className="error-message">{error}</p>}

      {!error && (
        <>
          <h1>Matched Grants</h1>
          <div className="grants-container">
            {matchedGrants.map((grant, index) => (
              <div key={index} className="grant-card">
                <div className="card-header">
                  <h2>{grant.name}</h2>
                  <p>Deadline: {grant.deadline ? new Date(grant.deadline).toLocaleDateString() : 'No deadline specified'}</p>
                </div>
                <div className="card-body">
                  <h4>Documents Needed:</h4>
                  <ul>
                    {(grant.documents_needed || '').split(',').map((doc, docIndex) => (
                      <li key={docIndex}>{doc}</li>
                    ))}
                  </ul>
                  <h4>Steps to Apply:</h4>
                  <ol>
                    {(grant.steps_to_apply || '').split(',').map((step, stepIndex) => (
                      <li key={stepIndex}>{step}</li>
                    ))}
                  </ol>
                  <a href={grant.link} target="_blank" rel="noopener noreferrer" className="apply-link">Apply Here</a>
                </div>
              </div>
            ))}
          </div>

          <h1>Applied Grants Status</h1>
          <div className="applied-grants-container">
            {appliedGrants.map((grant, index) => (
              <div key={index} className="applied-grant-card">
                <div className="applied-card-header">
                  <h2>{grant.name}</h2>
                  <p>Status: {grant.current_status}</p>
                </div>
                <div className="status-bar">
                  <div className="progress" style={{ width: `${grant.status}%` }}></div>
                </div>
                <p className="status-text">{grant.status}% Complete</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;
