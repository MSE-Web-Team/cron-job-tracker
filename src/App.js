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
      <JobContainer>
        <h2>Current Jobs</h2>
        <RunningJob job_name={"Job #1"} start_time={new Date()}></RunningJob>
        <RunningJob job_name={"MAS student update"} start_time={new Date()}></RunningJob>
        <hr></hr>
        <Job status={"warning"} job_name={"Job naasdasd asd asd sad asds asdasd ame here"} description={"This is a test so that it wil work"}></Job>
        <hr></hr>
        <Job status={"error"} job_name={"Job naasdasd asd asd sad asds asdasd ame here"} description={"This is a test so that it wil work"}></Job>
        <Job status={"error"} job_name={"Job naasdasd asd asd sad asds asdasd ame here"} description={"This is a test so that it wil work"}></Job>
      </JobContainer>
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
