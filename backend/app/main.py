from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()


# ✅ Import API route modules
from app.api import explain, audit, test, chat
from app.api import chat  # 👈 adjust path if needed




# ✅ Initialize FastAPI app
app = FastAPI(
    title="HoloMentorX Agent API",
    description="FastAPI backend connected with multiple uAgents for explain, audit, test, and chat functionality.",
    version="1.0.0"
)

# ✅ Enable CORS for React or any frontend running on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React or other frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers from each microservice agent
app.include_router(explain.router, prefix="/explain", tags=["explain"])
app.include_router(audit.router, prefix="/audit", tags=["audit"])
app.include_router(test.router, prefix="/test", tags=["test"])
app.include_router(chat.router)

# ✅ Optional root endpoint
@app.get("/")
async def root():
    return {"message": "🚀 HoloMentorX backend is running!"}
