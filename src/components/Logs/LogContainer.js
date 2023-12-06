import React, { useState } from 'react';
import styles from '../commonStyles.module.css';

const LogContainer = ({ children }) => (
    <div className={styles.logFlex}>
        {children}
    </div>
);

export default LogContainer;