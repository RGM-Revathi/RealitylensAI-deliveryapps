# FACT CHECK | RealityLensAI — full-stack prototype

A React + Vite frontend and FastAPI backend for review sentiment, aspect mentions, perspective labels, candidate claims, and evidence-status messaging.

## Requirements
- Python 3.10+
- Node.js 20+ recommended

## Run on Windows

### Terminal 1: backend
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Backend docs: http://127.0.0.1:8000/docs

### Terminal 2: frontend
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal, usually http://localhost:5173.

## Configuration
- Frontend API base: `VITE_API_URL` (defaults to `http://127.0.0.1:8000`)
- Backend CORS origins: `CORS_ORIGINS` comma-separated list (defaults to local Vite origins)

## Important limitations
- Sentiment is a transparent keyword baseline, not a trained ML model.
- Aspect matching is keyword-based.
- Candidate claim extraction is sentence splitting, not semantic fact verification.
- All claims are marked "Insufficient evidence" because no external evidence sources are queried.
- SQLite is used by default and stores records in `backend/realitylens.db`.
- Demo place names/review counts shown in the interface are illustrative, not verified real-world data.
- This is a local prototype, not production-ready. Add authentication, authorization, rate limiting, robust evidence retrieval, monitoring, privacy controls, backups, and deployment configuration before public launch.
