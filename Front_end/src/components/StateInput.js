import React from "react";

const StateInput = ({ state, setState }) => {
  return (
    <div>
      <label htmlFor="state">State:</label>
      <input
        type="text"
        id="state"
        value={state}
        onChange={(e) => setState(e.target.value)}
      />
    </div>
  );
};

export default StateInput;
