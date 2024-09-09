import React, { useState } from "react";
import "./App.css"; // Main App styling
import StateInput from "./components/StateInput";
import "./components/StateInput.css"; // Styling for StateInput
import DateInput from "./components/DateInput";
import "./components/DateInput.css"; // Styling for DateInput
import RainfallInput from "./components/RainfallInput";
import "./components/RainfallInput.css"; // Styling for RainfallInput
import SubmitButton from "./components/SubmitButton";
import "./components/SubmitButton.css"; // Styling for SubmitButton

function App() {
  const [state, setState] = useState("");
  const [date, setDate] = useState("");
  const [rainfall, setRainfall] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ state, date, rainfall });
    // You can call an API or perform other actions here
  };

  return (
    <div className="App">
      <h1>Water Level Predictor</h1>
      <form onSubmit={handleSubmit}>
        <StateInput state={state} setState={setState} />
        <DateInput date={date} setDate={setDate} />
        <RainfallInput rainfall={rainfall} setRainfall={setRainfall} />
        <SubmitButton />
      </form>
    </div>
  );
}

export default App;
