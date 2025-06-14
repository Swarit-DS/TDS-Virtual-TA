import fetch from 'node-fetch';
export const myTaProvider = {
  id: "my-ta-api",
  description: "Custom API for TDS Virtual TA",
  async callApi(prompt, context) {
    const response = await fetch("https://tds-virtual-ta-1pw1.onrender.com/api/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    const result = await response.json();
    return {
      output: result.answer,
    };
  },
};
