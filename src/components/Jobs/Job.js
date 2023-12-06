import React, { useState } from 'react';
import styles from '../commonStyles.module.css';

const Job = ({ status, job_name, description }) => {

    let statusColor;

    switch (status) {
        case 'error':
            statusColor = styles.error;
            break;
        case 'success':
            statusColor = styles.success;
            break;
        case 'warning':
            statusColor = styles.warning;
            break;
        default:
            statusColor = 'default';
    }

    const statusStyle = {
        color: statusColor,
    };

    const jobInfo = {
        name:job_name,
        description: description
    }


    return (
        <div className={styles.jobContainer}>
            {status && (
            <div className={`${styles.status} ${statusStyle.color}`}>
                
            </div>
            )}
            <p className={styles.name}>{jobInfo.name}</p>
            <p className={styles.desc}>{jobInfo.description}</p>
        </div>
    );
};

export default Job;
