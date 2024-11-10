import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './Dashboard.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Dashboard() {
  const matchedGrants = [
    { name: 'Healthcare Support Grant', deadline: 'December 31, 2024', documentsNeeded: ['ID Proof', 'Income Certificate', 'Medical Records'], stepsToApply: ['Fill out the application form', 'Attach required documents', 'Submit to the nearest office'], link: 'https://example.com/healthcare-support' },
    { name: 'Education Assistance Grant', deadline: 'January 15, 2025', documentsNeeded: ['Proof of Enrollment', 'ID Proof', 'Income Certificate'], stepsToApply: ['Complete the online application', 'Attach supporting documents', 'Wait for approval'], link: 'https://example.com/education-assistance' },
    { name: 'Housing Assistance Program', deadline: 'March 1, 2025', documentsNeeded: ['Rental Agreement', 'Income Certificate', 'ID Proof'], stepsToApply: ['Contact your local housing authority', 'Submit the application form', 'Provide necessary documents'], link: 'https://example.com/housing-assistance' },
    { name: 'Small Business Grant', deadline: 'April 15, 2025', documentsNeeded: ['Business License', 'Financial Statements', 'ID Proof'], stepsToApply: ['Complete application', 'Attach financial statements', 'Submit to local business office'], link: 'https://example.com/small-business' },
    { name: 'Energy Efficiency Grant', deadline: 'May 30, 2025', documentsNeeded: ['Home Ownership Proof', 'ID Proof', 'Energy Audit Report'], stepsToApply: ['Submit energy audit report', 'Complete application form', 'Submit to energy department'], link: 'https://example.com/energy-efficiency' },
    { name: 'Environmental Conservation Fund', deadline: 'June 15, 2025', documentsNeeded: ['Project Proposal', 'Financial Statements'], stepsToApply: ['Submit proposal', 'Provide financial statements', 'Submit online application'], link: 'https://example.com/environmental-conservation' },
    { name: 'Technology Innovation Grant', deadline: 'July 20, 2025', documentsNeeded: ['Business Plan', 'Proof of Concept'], stepsToApply: ['Complete application form', 'Attach business plan', 'Submit online'], link: 'https://example.com/technology-innovation' },
    { name: 'Rural Development Grant', deadline: 'August 10, 2025', documentsNeeded: ['Community Approval', 'Budget Plan'], stepsToApply: ['Complete application', 'Submit budget plan', 'Approval from local council'], link: 'https://example.com/rural-development' },
    { name: 'Arts and Culture Fund', deadline: 'September 5, 2025', documentsNeeded: ['Project Proposal', 'Portfolio'], stepsToApply: ['Submit proposal', 'Attach portfolio', 'Await review'], link: 'https://example.com/arts-culture' },
    { name: 'Student Scholarship Program', deadline: 'October 1, 2025', documentsNeeded: ['Enrollment Proof', 'Academic Records'], stepsToApply: ['Submit application form', 'Attach records', 'Wait for decision'], link: 'https://example.com/student-scholarship' },
    { name: 'Urban Renewal Project Fund', deadline: 'November 18, 2025', documentsNeeded: ['Project Plan', 'Community Approval'], stepsToApply: ['Submit project plan', 'Receive community approval', 'Submit to city council'], link: 'https://example.com/urban-renewal' },
    { name: 'Public Health Initiative Grant', deadline: 'December 15, 2025', documentsNeeded: ['Health Project Proposal', 'Community Support Letter'], stepsToApply: ['Submit proposal', 'Attach support letter', 'Submit to health department'], link: 'https://example.com/public-health' },
    { name: 'Agricultural Development Grant', deadline: 'January 10, 2026', documentsNeeded: ['Farm Ownership Proof', 'Agricultural Plan'], stepsToApply: ['Complete application', 'Attach plan', 'Submit to agriculture department'], link: 'https://example.com/agriculture' },
    { name: 'Youth Empowerment Grant', deadline: 'February 20, 2026', documentsNeeded: ['Project Proposal', 'Community Endorsement'], stepsToApply: ['Submit proposal', 'Attach endorsement', 'Submit to youth department'], link: 'https://example.com/youth-empowerment' },
    { name: 'Elderly Support Program', deadline: 'March 5, 2026', documentsNeeded: ['ID Proof', 'Medical Records'], stepsToApply: ['Complete application form', 'Attach medical records', 'Submit to support office'], link: 'https://example.com/elderly-support' }
  ];

  const appliedGrants = [
    { name: 'Childcare Support Grant', status: 70, currentStatus: 'In Review' },
    { name: 'Food Assistance Program', status: 40, currentStatus: 'Pending Verification' },
    { name: 'COVID Relief Fund', status: 90, currentStatus: 'Final Approval' },
    { name: 'Startup Innovation Grant', status: 60, currentStatus: 'Under Evaluation' },
    { name: 'Disability Assistance Grant', status: 80, currentStatus: 'Review Complete' },
    { name: 'Community Development Fund', status: 55, currentStatus: 'Pending Approval' },
    { name: 'Public Library Grant', status: 45, currentStatus: 'In Review' },
    { name: 'Environmental Restoration Fund', status: 30, currentStatus: 'Awaiting Documentation' },
    { name: 'Small Business Recovery Grant', status: 75, currentStatus: 'In Progress' },
    { name: 'Local Art Funding Program', status: 50, currentStatus: 'Under Consideration' }
  ];

  const newGrantsData = {
    labels: ['August', 'September', 'October', 'November', 'December'],
    datasets: [{ label: 'New Grants Added', data: [3, 5, 2, 8, 4], backgroundColor: '#4CAF50', borderRadius: 5 }],
  };

  const chartOptions = {
    responsive: true,
    plugins: { legend: { display: false } },
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-row">
        <div className="summary-section">
          <div className="summary-card">
            <h2>{matchedGrants.length}</h2>
            <p>Available Grants</p>
          </div>
          <div className="summary-card">
            <h2>{appliedGrants.length}</h2>
            <p>Grants Applied</p>
          </div>
          <div className="summary-card">
            <h2>5</h2>
            <p>New Grants This Month</p>
          </div>
        </div>

        <div className="chart-card">
          <h2>New Grants Added Over the Past Months</h2>
          <Bar data={newGrantsData} options={chartOptions} />
        </div>

        <div className="tips-card">
          <h2>Tips for Successful Grant Applications</h2>
          <ul>
            <li>Ensure all required documents are organized and up-to-date.</li>
            <li>Double-check deadlines to avoid missing important dates.</li>
            <li>Be thorough and honest in all application details.</li>
            <li>Follow up after submission to track the application status.</li>
          </ul>
        </div>
      </div>

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

      <div className="testimonials-section">
        <h2>User Testimonials</h2>
        <blockquote>"Applying for the Housing Assistance Program was so easy and straightforward!" – Jane D.</blockquote>
        <blockquote>"The Healthcare Support Grant helped my family immensely. Thank you!" – Mark S.</blockquote>
        <blockquote>"This platform made it simple to find and apply for the grants I needed." – Emily R.</blockquote>
      </div>
    </div>
  );
}

export default Dashboard;
