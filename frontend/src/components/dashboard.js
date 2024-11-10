import React from 'react';
import './Dashboard.css';

function Dashboard() { /// Update the cards page from the API
  const matchedGrants = [
    {
      name: 'Healthcare Support Grant',
      deadline: 'December 31, 2024',
      documentsNeeded: ['ID Proof', 'Income Certificate', 'Medical Records'],
      stepsToApply: ['Fill out the application form', 'Attach required documents', 'Submit to the nearest office'],
      link: 'https://example.com/healthcare-support'
    },
    {
      name: 'Education Assistance Grant',
      deadline: 'January 15, 2025',
      documentsNeeded: ['Proof of Enrollment', 'ID Proof', 'Income Certificate'],
      stepsToApply: ['Complete the online application', 'Attach supporting documents', 'Wait for approval'],
      link: 'https://example.com/education-assistance'
    },
    {
      name: 'Housing Assistance Program',
      deadline: 'March 1, 2025',
      documentsNeeded: ['Rental Agreement', 'Income Certificate', 'ID Proof'],
      stepsToApply: ['Contact your local housing authority', 'Submit the application form', 'Provide necessary documents'],
      link: 'https://example.com/housing-assistance'
    }
  ];

  const appliedGrants = [
    {
      name: 'Childcare Support Grant',
      status: 70,
      currentStatus: 'In Review'
    },
    {
      name: 'Food Assistance Program',
      status: 40,
      currentStatus: 'Pending Verification'
    }
  ];

  return (
    <div className="dashboard-container">
      <h1>Matched Grants</h1>
      <div className="grants-container">
        {matchedGrants.map((grant, index) => (
          <div key={index} className="grant-card">
            <div className="card-header">
              <h2>{grant.name}</h2>
              <p>Deadline: {grant.deadline}</p>
            </div>
            <div className="card-body">
              <h4>Documents Needed:</h4>
              <ul>
                {grant.documentsNeeded.map((doc, docIndex) => (
                  <li key={docIndex}>{doc}</li>
                ))}
              </ul>
              <h4>Steps to Apply:</h4>
              <ol>
                {grant.stepsToApply.map((step, stepIndex) => (
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
              <p>Status: {grant.currentStatus}</p>
            </div>
            <div className="status-bar">
              <div className="progress" style={{ width: `${grant.status}%` }}></div>
            </div>
            <p className="status-text">{grant.status}% Complete</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
