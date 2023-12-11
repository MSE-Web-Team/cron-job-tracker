import logo from './logo.svg';
import './App.css';
import Job from './components/Jobs/Job';
import RunningJob from './components/Jobs/RunningJob';
import JobContainer from './components/Jobs/JobContainer';
import LogMessage from './components/Logs/LogMessage';
import LogContainer from './components/Logs/LogContainer';

function App() {

  return (
    <div className="App">
      <JobContainer></JobContainer>
      <LogContainer>
        <h2>Current Logs</h2>
        <LogMessage status="error" name="EHIAHDIW" description={"asdasd"}></LogMessage>
        <LogMessage status="error" name="EHIAHDIW" description={"asdasd"}></LogMessage>
        <LogMessage status="error" name="EHIAHDIW" description={"asdasd"}></LogMessage>
        <LogMessage status="error" name="EHIAHDIW" description={"asdasd"}></LogMessage>
      </LogContainer>
      
    </div>
  );
}

export default App;
