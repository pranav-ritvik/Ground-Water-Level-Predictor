import React from "react";

const DateInput = ({ date, setDate }) => {
  return (
    <div>
      <label htmlFor="date">Date (yyyy-mm):</label>
      <input
        type="month"
        id="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />
    </div>
  );
};

export default DateInput;
