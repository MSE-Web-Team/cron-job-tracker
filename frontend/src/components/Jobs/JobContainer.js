import React, { useState } from 'react';
import styles from '../commonStyles.module.css';

const JobContainer = ({ children }) => (
    <div className={styles.jobFlex}>
        {children}
    </div>
);

export default JobContainer;