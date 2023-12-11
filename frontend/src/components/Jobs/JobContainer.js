import React, { useState, useEffect } from 'react';
import RunningJob from './RunningJob';
import Job from './Job';
import styles from '../commonStyles.module.css';

const JobContainer = ({ status }) => {
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

  const filteredJobs = jobs.filter(job => job.status === status);

  return (
    <div className={styles.jobFlex}>
      <h2>Jobs - {status}</h2>
      {filteredJobs.map(job => {
        const { id, process_name, start_time, status, description } = job;

        if (status === 'RUNNING') {
          return (
            <RunningJob
              key={id}
              job_name={process_name}
              start_time={new Date(start_time)}
            />
          );
        } else {
          return (
            <Job
              key={id}
              status={status.toLowerCase()}
              job_name={process_name}
              description={description}
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
