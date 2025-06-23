import React from "react";
import { createRoot } from "react-dom/client";

function App(): JSX.Element {
  return <h1>Welcome to movieindex</h1>;
}

const container = document.getElementById("root");
if (!container) {
  throw new Error("Root container not found");
}
const root = createRoot(container);
root.render(<App />);
