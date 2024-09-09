import React from "react";

const RainfallInput = ({ rainfall, setRainfall }) => {
  return (
    <div>
      <label htmlFor="rainfall">Rainfall (mm):</label>
      <input
        type="number"
        id="rainfall"
        value={rainfall}
        onChange={(e) => setRainfall(e.target.value)}
      />
    </div>
  );
};

export default RainfallInput;
