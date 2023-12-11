import React, { useState, useEffect } from 'react';
import RunningJob from './RunningJob';
import Job from './Job';
import styles from '../commonStyles.module.css';

const JobContainer = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('/api/jobs');
        const data = await response.json();

        // Check if the 'jobs' property exists in the JSON response
        if (data && data.jobs) {
          setJobs(data.jobs);
        } else {
          console.error('Malformed JSON response from the server:', data);
        }
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div className={styles.jobFlex}>
      <h2>Current Jobs</h2>
      {jobs.map(job => {
        const { id, process_name, start_time, status } = job;

        if (status === 'SUCCESS' || status === 'INFO') {
          return (
            <RunningJob
              key={id}
              job_name={process_name}
              start_time={new Date(start_time)}
            />
          );
        } else if (status === 'ERROR' || status === 'UNKNOWN') {
          return (
            <Job
              key={id}
              status={status.toLowerCase()}
              job_name={process_name}
              description={`This is a test so that it will work for status: ${status}`}
            />
          );
        }

        // Add more conditions for other statuses if needed
        return null;
      })}
      <hr />
      {/* Render other job components as needed */}
    </div>
  );
};

// Similar component for LogContainer

export default JobContainer;
