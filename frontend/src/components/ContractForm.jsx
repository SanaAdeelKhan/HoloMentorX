export default function ContractForm({ code, onCodeChange }) {
  return (
    <div className="w-full max-w-2xl space-y-4">
      <textarea
        rows={10}
        value={code}
        onChange={(e) => onCodeChange(e.target.value)} // 🔄 Live update parent state
        placeholder="Paste your Qubic C++ smart contract code here..."
        className="w-full p-4 text-sm bg-gray-800 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="button"
        onClick={() => alert("✅ Contract loaded. Now choose an action below.")}
        className="w-full py-2 bg-blue-500 text-black font-semibold rounded-xl hover:bg-blue-600 transition"
      >
        Load Contract
      </button>
    </div>
  );
}
