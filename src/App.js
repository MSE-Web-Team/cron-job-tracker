import logo from './logo.svg';
import './App.css';
import Job from './components/Jobs/Job';
import RunningJob from './components/Jobs/RunningJob';
import JobContainer from './components/Jobs/JobContainer';

function App() {

  return (
    <div className="App">
      <JobContainer>
        <h1>Current Jobs</h1>
        <RunningJob job_name={"Job #1"} start_time={new Date()}></RunningJob>
        <RunningJob job_name={"MAS student update"} start_time={new Date()}></RunningJob>
        <hr></hr>
        <Job status={"warning"} job_name={"Job naasdasd asd asd sad asds asdasd ame here"} description={"This is a test so that it wil work"}></Job>
        <hr></hr>
        <Job status={"error"} job_name={"Job naasdasd asd asd sad asds asdasd ame here"} description={"This is a test so that it wil work"}></Job>
        <Job status={"error"} job_name={"Job naasdasd asd asd sad asds asdasd ame here"} description={"This is a test so that it wil work"}></Job>
      </JobContainer>
    </div>
  );
}

export default App;
