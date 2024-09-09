import React, { useState } from "react";
import "./WaterLevelForm.css";

const WaterLevelForm = () => {
  const [state, setState] = useState("");
  const [date, setDate] = useState("");
  const [rainfall, setRainfall] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const requestData = {
      year_month: date,
      location: state,
      rainfall_level: rainfall,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();
      setPrediction(data.predicted_groundwater_level);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="input-container">
          <label htmlFor="state">State:</label>
          <input
            type="text"
            id="state"
            value={state}
            onChange={(e) => setState(e.target.value)}
            placeholder="Enter state (e.g., Andhra Pradesh)"
          />
        </div>

        <div className="input-container">
          <label htmlFor="date">Date (yyyy-mm):</label>
          <input
            type="month"
            id="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input-container">
          <label htmlFor="rainfall">Rainfall (mm):</label>
          <input
            type="number"
            id="rainfall"
            value={rainfall}
            onChange={(e) => setRainfall(e.target.value)}
            placeholder="Enter rainfall in mm"
          />
        </div>

        <button type="submit" className="submit-button">
          Predict Water Level
        </button>
      </form>

      {prediction && (
        <div className="prediction-result">
          <h3>Predicted Groundwater Level: {prediction}</h3>
        </div>
      )}
    </div>
  );
};

export default WaterLevelForm;
