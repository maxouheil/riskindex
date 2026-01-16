from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
from pathlib import Path
from app.api.routes import router
import uvicorn
import logging
import sys
from datetime import datetime
import json

# Configuration des logs Python standard pour affichage dans le terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv(Path(__file__).parent.parent / ".env")

app = FastAPI(
    title="Risk Index API",
    description="API pour évaluer le risque économique des pays basé sur les données World Bank",
    version="1.0.0"
)

# Ajouter compression GZip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour logger toutes les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # #region agent log
    LOG_PATH = '/Users/sou/Desktop/CURSOR/RiskIndex/.cursor/debug.log'
    start_time = datetime.now()
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "A",
            "location": "main.py:middleware",
            "message": "HTTP request received",
            "data": {
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "client": request.client.host if request.client else None
            },
            "timestamp": int(start_time.timestamp() * 1000)
        }
        with open(LOG_PATH, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except:
        pass
    # #endregion
    logger.info(f"🔵 {request.method} {request.url.path} - Client: {request.client.host if request.client else 'unknown'}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "A",
            "location": "main.py:middleware",
            "message": "HTTP request completed",
            "data": {
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time_seconds": process_time
            },
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
        with open(LOG_PATH, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except:
        pass
    # #endregion
    logger.info(f"🟢 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}s")
    
    return response

# Inclure les routes
app.include_router(router, prefix="/api", tags=["risk"])


@app.get("/")
async def root():
    return {
        "message": "Risk Index API",
        "version": "1.0.0",
        "endpoints": {
            "france_risk": "/api/risk/france",
            "france_history": "/api/risk/france/history",
            "south_africa_weekly": "/api/geopolitical/south-africa/weekly"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
