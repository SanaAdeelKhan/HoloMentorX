# 🧠 HoloMentorX – The Qubic AI Knowledge Guider

**HoloMentorX** is a futuristic AI-powered agentic system that helps users understand, audit, and test **C++ smart contracts** deployed on the **Qubic Network**. Built using an agent-based architecture with Fetch.ai’s uAgents and ASI:One identity layer, it features intelligent explanation, audit, and test workflows with ultra-fast AI reasoning powered by Groq + LLaMA.

---

## 🌟 What is HoloMentorX?

HoloMentorX empowers developers, learners, and auditors in the decentralized Web3 space. It acts like a holographic sci-fi mentor, offering:

- 🔍 Step-by-step understanding of Qubic C++ smart contracts
- 🛡️ Contract audits to detect vulnerabilities
- 🧪 Test case generation for smart contract verification
- 🌐 Real-time contract querying for tick-based logic
- 🤖 Interoperable agent framework using Fetch.ai + ASI:One
- 🎮 Holographic UI built with modern frontend tools

---

## 🛠️ Core Features

| Feature        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| 🧠 ExplainAgent | Explains Qubic C++ contracts step-by-step using LLaMA via Groq              |
| 🛡️ AuditAgent   | Identifies common bugs and logic flaws                                      |
| 🧪 TestAgent    | Generates test cases and fuzz inputs                                        |
| 🌐 Agentverse   | Decentralized agent registry and communication via ASI:One                 |
| 🎮 Holo UI      | Interactive React + Tailwind interface with glowing, futuristic visuals     |

---

## 👨‍💻 Tech Stack

| Layer       | Tech Stack                                                                 |
|-------------|-----------------------------------------------------------------------------|
| Frontend    | React, TailwindCSS, Vite                                                    |
| Backend     | FastAPI, Python                                                             |
| Agents      | Fetch.ai uAgents, ASI:One, Agentverse                                       |
| AI Models   | Groq + LLaMA (primary)                  |
| Contracts   | C++ on Qubic Testnet                                                        |

---

## 📁 Folder Structure

### 🔙 `/backend`
backend/
├── app.py # FastAPI server with /submit endpoint
├── explain_agent.py # ExplainAgent using uAgents
├── audit_agent.py # AuditAgent (optional integration)
├── test_agent.py # TestAgent for test generation
├── requirements.txt # Python dependencies
└── utils/
└── parser.py # Code parsing or preprocessing logic


### 🌐 `/frontend`
frontend/
├── index.html # Entry HTML with root div
├── vite.config.js # Vite setup
├── package.json # Frontend dependencies
├── tailwind.config.js # TailwindCSS config
├── src/
│ ├── main.jsx # React app entry point
│ ├── App.jsx # Root component
│ ├── components/
│ │ └── ContractForm.jsx # Code input and submit button
│ │ └── ExplanationView.jsx # Displays AI output
│ └── assets/ # Logo, background effects
└── styles/
└── globals.css # TailwindCSS + custom styles

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/TeamGreen/HoloMentorX.git
cd HoloMentorX

## **🔹 Backend Setup**
cd backend
python -m venv venv310
source venv310/bin/activate      # On Windows: .\venv310\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

## **🔹 Frontend Setup**
cd frontend
npm install
npm run dev

## **👥 Team Green – Qubic Track**
Name	                Role
Sana	      Team Lead, System Architect
Saad	      Frontend Lead (Holo UI, Vite, Tailwind)
Noor    	  C++ Contract Developer (Qubic Smart Chain)
Nimra       AI Agent Developer (Explain, Audit Agents)
Safwan     	Backend & Embedded Integrations
Zain        Agent Operations & Deployment

## **🏁 Hackathon Info**
Track: Qubic Track — RAISE YOUR HACK 2025

Platform: ASI:One + Agentverse (Fetch.ai)

Requirements:

C++ Smart Contracts on Qubic Testnet

Agent-based messaging architecture

AI reasoning via Groq + LLaMA

## 📄 License
MIT — Free to use, open-source

"The jungle had owls. The blockchain has mentors." — Team Green 🦉🌐
