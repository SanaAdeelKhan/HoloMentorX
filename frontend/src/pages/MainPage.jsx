import { useState } from "react";
import Avatar, { genConfig } from "react-nice-avatar";
import ReactMarkdown from "react-markdown";
import ContractForm from "../components/ContractForm";
import MainChat from "../components/MainChat";

export default function MainPage() {
  const avatarConfig = genConfig();
  const [mode, setMode] = useState(null);
  const [code, setCode] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleMode = async (selectedMode) => {
    if (!code) {
      alert("Please paste or load a contract first.");
      return;
    }

    setMode(selectedMode);
    setLoading(true);

    let endpoint = "";
    switch (selectedMode) {
      case "Explain":
        endpoint = "/explain";
        break;
      case "Audit":
        endpoint = "/audit";
        break;
      case "Test":
        endpoint = "/test";
        break;
      default:
        endpoint = "/explain";
    }

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await res.json();

      const explanation =
        data.asi_explanation?.trim() ||
        data.message?.trim() || // fallback if message used instead
        "❌ No explanation received.";
      setResult(explanation);
      setHistory((prev) => [...prev, { mode: selectedMode, result: explanation }]);
    } catch (err) {
      console.error(err);
      setResult("❌ Error contacting agent.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-800 text-white">
      {/* Sidebar */}
      <div className="p-6 flex flex-col items-center">
        <Avatar {...avatarConfig} style={{ width: 80, height: 80 }} />
        <h2 className="mt-4 text-xl font-semibold">HoloMentorX</h2>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6 space-y-6">
        <ContractForm code={code} onCodeChange={(c) => setCode(c)} />

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4">
          <button onClick={() => handleMode("Explain")} className="px-4 py-2 bg-blue-800 hover:bg-blue-900 text-black rounded">
            Explain
          </button>
          <button onClick={() => handleMode("Audit")} className="px-4 py-2 bg-yellow-700 hover:bg-yellow-800 text-black rounded">
            Audit
          </button>
          <button onClick={() => handleMode("Test")} className="px-4 py-2 bg-green-800 hover:bg-green-900 text-black rounded">
            Test
          </button>
        </div>

        {/* Loading */}
        {loading && <div className="text-yellow-400 text-lg">⏳ Loading, please wait...</div>}

        {/* Result Output */}
        {!loading && result && (
          <div className="bg-gray-700 p-4 rounded border border-green-500">
            <h4 className="text-lg font-bold text-green-400 mb-2">🧠 ASI:One</h4>
            <ReactMarkdown className="prose prose-invert whitespace-pre-wrap break-words max-w-none">
              {result}
            </ReactMarkdown>
          </div>
        )}

        {/* History */}
        {history.length > 0 && (
          <div className="mt-8 space-y-4">
            <h3 className="text-xl text-gray-300">📚 Previous Results:</h3>
            {history.map((entry, index) => (
              <div key={index} className="border-t border-gray-600 pt-4">
                <h4 className="text-lg mb-2">🔁 {entry.mode}</h4>
                <div className="bg-gray-700 p-3 rounded border border-green-600 overflow-auto">
                  <ReactMarkdown className="prose prose-invert whitespace-pre-wrap break-words max-w-none">
                    {entry.result}
                  </ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Chat Section */}
        <div className="mt-6">
          <MainChat
            onSend={(msg, reply) => {
              fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg, contract: code }),
              })
                .then((r) => r.json())
                .then((d) => reply(d.answer)) // ✅ Matches new response key
                .catch((_) => reply("❌ Error contacting assistant"));
            }}
          />
        </div>
      </div>

      {/* Right Hologram */}
      <div className="p-6 hidden lg:flex items-center justify-center">
        <img src="/Hologram3.jpeg" alt="Hologram" className="max-w-xs rounded-lg shadow-lg" />
      </div>
    </div>
  );
}
