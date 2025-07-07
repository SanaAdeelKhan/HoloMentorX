// src/App.jsx
import { useState } from "react";
import HomePage from "./pages/HomePage";
import MainPage from "./pages/MainPage";

export default function App() {
  const [started, setStarted] = useState(false);
  return (
    <div className="h-screen">
      {started ? <MainPage /> : <HomePage onStart={() => setStarted(true)} />}
    </div>
  );
}
