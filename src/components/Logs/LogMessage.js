import React, { useState } from 'react';

const LogMessage = () => {
  // State example
  const [count, setCount] = useState(0);

  // Event handler
  const handleIncrement = () => {
    setCount(count + 1);
  };

  return (
    <div>
      <h1>Hello, World!</h1>
      <p>Count: {count}</p>
      <button onClick={handleIncrement}>Increment</button>
    </div>
  );
};

export default LogMessage;
