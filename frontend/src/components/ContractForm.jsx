import { useState } from 'react';

export default function ContractForm() {
  const [contract, setContract] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult('');

    try {
      const response = await fetch('http://localhost:8000/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: contract }),
      });

      const data = await response.json();
      setResult(data.explanation || '<p>No explanation received.</p>');
    } catch (err) {
      console.error(err);
      setResult('<p>❌ Error occurred while processing the contract.</p>');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl space-y-4">
      <textarea
        rows={10}
        value={contract}
        onChange={(e) => setContract(e.target.value)}
        placeholder="Paste your Qubic C++ smart contract code here..."
        className="w-full p-4 text-sm bg-gray-800 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        disabled={loading}
        className="w-full py-2 bg-blue-500 text-black font-semibold rounded-xl hover:bg-blue-600 transition"
      >
        {loading ? 'Analyzing...' : 'Explain Contract'}
      </button>

      {result && (
        <div className="mt-4 p-4 bg-gray-900 text-white rounded-xl">
          <h2 className="text-lg font-bold mb-4">🧠 Explanation:</h2>
          <article
            className="prose prose-invert max-w-none text-sm"
            dangerouslySetInnerHTML={{ __html: result }}
          />
        </div>
      )}
    </form>
  );
}
