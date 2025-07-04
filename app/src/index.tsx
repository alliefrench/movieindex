import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";

function App(): JSX.Element {
  const [scaryResponse, setScaryResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchScaryData = async () => {
      try {
        const response = await fetch("http://localhost:8000/scary");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setScaryResponse(data.message);
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
        setLoading(false);
      }
    };

    fetchScaryData();
  }, []);

  if (loading) return <h1>Loading scary content...</h1>;
  if (error) return <h1>Error: {error}</h1>;

  return (
    <div>
      <h1>Welcome to movieindex</h1>
      <h2>Scary Response:</h2>
      <p>{scaryResponse}</p>
    </div>
  );
}

const container = document.getElementById("root");
if (!container) {
  throw new Error("Root container not found");
}
const root = createRoot(container);
root.render(<App />);
