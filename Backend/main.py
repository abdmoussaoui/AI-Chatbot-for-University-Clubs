from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from rag_chain import get_intelligent_response, load_all_models, ALL_CLUBS
from visualization import generate_recommendation_plot
import uvicorn
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("✅ Application starting up...")
    try:
        load_all_models()
    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        raise
    yield
    logger.info("🛑 Application shutting down...")

app = FastAPI(lifespan=lifespan)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class SessionEntry(BaseModel):
    user_query: str
    response: str
    action: str

class ChatRequest(BaseModel):
    message: str
    session: List[SessionEntry]

class ChatResponse(BaseModel):
    response: str
    recommendation: Optional[Dict[str, Optional[str]]]
    club_scores: Optional[Dict[str, float]]
    plot_url: Optional[str]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received request: {request.dict()}")
    try:
        user_message = request.message
        session = request.session

        result = get_intelligent_response(user_message, session)
        logger.info(f"Result from get_intelligent_response: {result}")

        plot_url = None
        if result.get("recommendation") and result["recommendation"].get("club"):
            club_name = result["recommendation"]["club"]
            club_scores = result.get("club_scores", {})
            logger.info(f"Generating plot for club: {club_name}, scores: {club_scores}")
            try:
                plot_path = generate_recommendation_plot(club_name, ALL_CLUBS, club_scores)
                plot_url = f"/{plot_path}"
                logger.info(f"Plot generated at: {plot_url}")
            except Exception as e:
                logger.warning(f"Failed to generate plot: {e}")
                plot_url = None

        return ChatResponse(
            response=result.get("response", ""),
            recommendation=result.get("recommendation"),
            club_scores=result.get("club_scores"),
            plot_url=plot_url
        )
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error occurred: {str(e)}")

@app.get("/clubs")
async def get_all_clubs():
    return ALL_CLUBS

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)