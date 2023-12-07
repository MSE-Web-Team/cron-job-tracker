import React, { useState, useEffect } from 'react';
import styles from '../commonStyles.module.css';

const RunningJob = ({ job_name, start_time }) => {
  const jobInfo = {
    name: job_name,
    start_time: start_time,
  };

  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      const currentTime = new Date();
      const startTime = new Date(jobInfo.start_time);

      // Check if startTime is a valid date
      if (isNaN(startTime.getTime())) {
        console.error(`Invalid start_time: ${jobInfo.start_time}`);
        return;
      }

      const elapsedMilliseconds = currentTime - startTime;
      const elapsedSeconds = Math.floor(elapsedMilliseconds / 1000);
      setElapsedTime(elapsedSeconds);
    }, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, [jobInfo.start_time]);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    return `${hours}h ${minutes}m ${remainingSeconds}s`;
  };

  return (
    <div className={styles.jobContainer}>
      <div>
        <div className={styles.progressCircle}></div>

      </div>
      <div className={styles.jobInfo}>
        <p className={styles.name}>{jobInfo.name}</p>
        <p className={styles.desc}>Start time: {jobInfo.start_time.toString()}</p>
        {isNaN(elapsedTime) ? (
          <p className={styles.desc}>Elapsed time: Invalid start time</p>
        ) : (
          <p className={styles.desc}>Elapsed time: {formatTime(elapsedTime)}</p>
        )}
      </div>
    </div>
  );
};

export default RunningJob;