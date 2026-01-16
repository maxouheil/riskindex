from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
from pathlib import Path
from app.api.routes import router
import uvicorn
import logging
import sys
import os
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
# Permettre les origines locales et Vercel (via variable d'environnement)
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
]
# Ajouter l'origine Vercel si définie
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    # Ajouter avec et sans https
    cors_origins.extend([
        f"https://{vercel_url}",
        f"http://{vercel_url}",
    ])
# Ajouter l'URL du frontend Vercel si définie
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    cors_origins.extend([
        frontend_url,
        frontend_url.replace("https://", "http://"),
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour logger toutes les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # #region agent log
    # Log uniquement en développement (chemin local)
    LOG_PATH = os.getenv("DEBUG_LOG_PATH", "/tmp/debug.log")
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
