import logo from './logo.svg';
import './App.css';
import Job from './components/Jobs/Job';

import JobContainer from './components/Jobs/JobContainer';
import LogMessage from './components/Logs/LogMessage';
import LogContainer from './components/Logs/LogContainer';

function App() {

  return (
    <div className="App">
      <JobContainer status="RUNNING"></JobContainer>
    </div>
  );
}

export default App;
