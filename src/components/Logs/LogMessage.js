import React, { useState } from 'react';
import styles from '../commonStyles.module.css';

const LogMessage = ({ status, name, description }) => {

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
        name:name,
        description: description
    }


    return (
        <div className={styles.logContainer}>
            {status && (
            <div className={`${styles.status} ${statusStyle.color} ${styles.smallStatus}`}>
                
            </div>
            )}
              <p className={styles.name}>{jobInfo.name}</p>
              <p className={styles.desc}>{jobInfo.description}</p>
        </div>
    );
};

export default LogMessage;
