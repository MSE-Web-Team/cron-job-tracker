import React, { useState, useEffect } from 'react';

const JobContainer = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('/api/jobs');
        const data = await response.json();
        setJobs(data.jobs);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div>
      <h2>Current Jobs</h2>
      {jobs.map(job => (
        <RunningJob
          key={job.id}
          job_name={job.process_name}
          start_time={new Date(job.start_time)}
        />
      ))}
      <hr></hr>
      {/* Render other job components as needed */}
    </div>
  );
};

// Similar component for LogContainer

export default JobContainer;
