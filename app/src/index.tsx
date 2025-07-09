import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";

interface User {
  id: string;
  name: string;
  email: string;
  avatar_url?: string;
}

function App(): JSX.Element {
  const [scaryResponse, setScaryResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  // Get API URL from environment variables
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  // Check for token in URL and load user
  useEffect(() => {
    // Check if there's a token in the URL (from Google OAuth callback)
    const urlParams = new URLSearchParams(window.location.search);
    const urlToken = urlParams.get("token");

    if (urlToken) {
      setToken(urlToken);
      localStorage.setItem("token", urlToken);
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else {
      // Check localStorage for existing token
      const savedToken = localStorage.getItem("token");
      if (savedToken) {
        setToken(savedToken);
      }
    }
  }, []);

  // Load user info when token changes
  useEffect(() => {
    if (token) {
      fetchUserInfo(token);
    }
    fetchScaryData();
  }, [token]);

  const fetchScaryData = async () => {
    try {
      console.log("Fetching data from", `${API_URL}/scary`);
      const response = await fetch(`${API_URL}/scary`);
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

  const fetchUserInfo = async (userToken: string) => {
    try {
      const response = await fetch(`${API_URL}/auth/me?token=${userToken}`);
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (err) {
      console.error("Failed to fetch user info:", err);
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = `${API_URL}/auth/google`;
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
  };

  if (loading) return <h1>Loading scary content...</h1>;
  if (error) return <h1>Error: {error}</h1>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      {/* Header with user info or login button */}
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "30px",
          padding: "20px",
          borderBottom: "1px solid #eee",
        }}
      >
        <h1>🎬 Welcome to movieindex</h1>

        {user ? (
          <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
            {user.avatar_url && (
              <img
                src={user.avatar_url}
                alt={user.name}
                style={{ width: "40px", height: "40px", borderRadius: "50%" }}
              />
            )}
            <div>
              <div style={{ fontWeight: "bold" }}>{user.name}</div>
              <div style={{ fontSize: "0.9em", color: "#666" }}>
                {user.email}
              </div>
            </div>
            <button
              onClick={handleLogout}
              style={{
                padding: "8px 16px",
                backgroundColor: "#ff4444",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <button
            onClick={handleGoogleLogin}
            style={{
              padding: "12px 24px",
              backgroundColor: "#4285f4",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "16px",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            🚀 Login with Google
          </button>
        )}
      </header>

      {/* Main content */}
      <div>
        <h2>Scary Response:</h2>
        <p
          style={{
            fontSize: "18px",
            padding: "15px",
            backgroundColor: "#f5f5f5",
            borderRadius: "8px",
          }}
        >
          {scaryResponse}
        </p>

        <div
          style={{
            marginTop: "40px",
            padding: "20px",
            border: "1px solid #4caf50",
            borderRadius: "8px",
            backgroundColor: "#f0f8f0",
          }}
        >
          <h3>✅ Google OAuth Working!</h3>
          <p>Your authentication system is now powered by:</p>
          <ul>
            <li>
              🔐 <strong>Google OAuth 2.0</strong> - Secure login with Google
              accounts
            </li>
            <li>
              🗄️ <strong>Neon Database</strong> - User data stored in PostgreSQL
            </li>
            <li>
              🔑 <strong>JWT Tokens</strong> - Secure session management
            </li>
            <li>
              ⚡ <strong>FastAPI Backend</strong> - High-performance API
            </li>
            <li>
              ⚛️ <strong>React Frontend</strong> - Modern user interface
            </li>
          </ul>

          {user ? (
            <div
              style={{
                marginTop: "15px",
                padding: "15px",
                backgroundColor: "#e8f5e8",
                borderRadius: "6px",
              }}
            >
              <strong>🎉 You're logged in!</strong> Your user data is securely
              stored in Neon.
            </div>
          ) : (
            <div
              style={{
                marginTop: "15px",
                padding: "15px",
                backgroundColor: "#fff3cd",
                borderRadius: "6px",
              }}
            >
              <strong>
                👆 Click "Login with Google" to test the authentication flow!
              </strong>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const container = document.getElementById("root");
if (!container) {
  throw new Error("Root container not found");
}
const root = createRoot(container);
root.render(<App />);
