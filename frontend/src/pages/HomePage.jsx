// src/pages/HomePage.jsx
import Avatar, { genConfig } from "react-nice-avatar";
import { motion } from "framer-motion";

export default function HomePage({ onStart }) {
  const avatarConfig = genConfig();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-6">
      {/* Left side: Video */}
      <div className="w-1/2 pr-6">
        <video
          src="/Hologram2.mp4"
          autoPlay
          loop
          muted
          playsInline
          className="rounded-lg shadow-lg w-full"
        />
      </div>

      {/* Right side: Heading, tagline, avatar, button */}
      <div className="w-1/2 flex flex-col items-center text-center space-y-8">
        <Avatar {...avatarConfig} style={{ width: 120, height: 120 }} />
        <h1 className="text-6xl font-extrabold text-white">HoloMentorX</h1>
        <p className="text-2xl text-gray-300">
          Your AI‑Powered Mentor for Qubic Smart Contracts
        </p>
        <motion.button
          className="mt-2 px-8 py-4 bg-blue-500 text-black text-lg font-semibold rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
          whileHover={{ scale: 1.05 }}
          onClick={onStart}
        >
          Start
        </motion.button>
      </div>
    </div>
  );
}
