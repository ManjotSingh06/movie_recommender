# movie_recommender_system

## Overview

This repository contains a movie recommender web app with:
- Flask backend in `app.py`
- React frontend in `frontend/`
- precomputed recommendation artifacts: `movies_list.pkl` and `similarity.pkl`

## Added production deployment files

- `Dockerfile` — backend container definition
- `frontend/Dockerfile` — frontend production build container
- `docker-compose.yml` — local multi-service deployment
- `.dockerignore` / `frontend/.dockerignore` — container build exclusions
- `scripts/build_data.py` — build-time data artifact generator
- `.env.example` / `frontend/.env.example` — environment variable templates

## Local development setup

### Backend

1. Create a Python virtual environment:
   ```powershell
   python -m venv env
   .\env\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy the backend env template:
   ```powershell
   copy .env.example .env
   ```
4. Update `.env` with your OMDb API key and optional paths.
5. Run the backend:
   ```powershell
   flask run
   ```

### Frontend

1. Change into the frontend folder:
   ```powershell
   cd frontend
   ```
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Copy the frontend env template:
   ```powershell
   copy .env.example .env
   ```
4. Start the frontend dev server:
   ```powershell
   npm run dev
   ```

## Docker-based deployment

### Build and run both services

From the repository root:
```powershell
docker compose up --build
```

Frontend will be available at `http://localhost:4173` and backend at `http://localhost:5000`.

### Backend container

The backend container uses `gunicorn` for production-grade WSGI hosting.

### Frontend container

The frontend container builds the Vite app and serves static assets via Nginx.

## Data artifact generation

If you have the source dataset, generate serialized artifacts with:
```powershell
python .\scripts\build_data.py --dataset dataset.csv --movies-out movies_list.pkl --similarity-out similarity.pkl
```

## Environment variables

### Backend
- `OMDB_API_KEY` — OMDb API key used to fetch movie posters
- `MOVIES_PKL` — path to `movies_list.pkl`
- `SIMILARITY_PKL` — path to `similarity.pkl`
- `ALLOWED_ORIGINS` — allowed CORS origin(s), comma-separated
- `FLASK_RUN_PORT` — backend HTTP port

### Frontend
- `VITE_API_URL` — base backend API URL for the React app

## Notes

- Keep `.env` files out of source control and only commit `.env.example`.
- The `docker-compose.yml` file is designed for local CI-style deployment; adapt it to your cloud provider or Kubernetes as needed.

## Overview

This repository contains a movie recommender web app with:
- Flask backend in `app.py`
- React frontend in `frontend/`
- precomputed content similarity artifacts: `movies_list.pkl` and `similarity.pkl`

## Files created for production readiness

- `requirements.txt` — backend Python dependencies
- `.env.example` — backend environment variables template
- `frontend/.env.example` — frontend environment variables template

## Backend setup

1. Create a Python virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and update values:
   ```bash
   copy .env.example .env
   ```
4. Start the backend:
   ```bash
   flask run
   ```

> In production, do not use `flask run` for hosting. Use a production WSGI server such as Gunicorn or another deployment platform.

## Frontend setup

1. Change to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy the frontend env example:
   ```bash
   copy .env.example .env
   ```
4. Start the local frontend dev server:
   ```bash
   npm run dev
   ```

## Environment variables

### Backend
- `OMDB_API_KEY` — your OMDb API key
- `DATA_PATH` — path to the source dataset (for data generation workflows)
- `MOVIES_PKL` — movie artifact file
- `SIMILARITY_PKL` — similarity artifact file
- `ALLOWED_ORIGINS` — CORS origin for frontend access

### Frontend
- `VITE_API_URL` — base URL for the backend API

## Notes

- `movies_list.pkl` and `similarity.pkl` are generated from `Main.ipynb` using the dataset and feature engineering steps.
- Keep `.env` files out of source control. Only commit `.env.example`.
- If you add deployment automation, update `README.md` with your platform-specific commands.

## CI / CD with GitHub Actions and Render

This repository includes a GitHub Actions workflow at `.github/workflows/ci-cd.yml` that:
- installs backend dependencies
- builds and pushes Docker images for backend and frontend to GitHub Container Registry (GHCR)
- optionally triggers Render deploys using the Render API

To enable full automation, add the following repository secrets in GitHub:
- `RENDER_API_KEY` — API key from your Render account
- `RENDER_BACKEND_SERVICE_ID` — Render service ID for the backend service
- `RENDER_FRONTEND_SERVICE_ID` — Render service ID for the frontend site

If you prefer to deploy directly from the repo in Render, you can instead:
1. Add a new Web Service (Docker) pointing to this repo for the backend
   - set Root Directory to `/` or leave it blank
   - use `Dockerfile` at the repo root
2. Add a new Static Site for the frontend
   - set Root Directory to `frontend`
   - use build command `npm install && npm run build`
   - set publish directory to `dist`
3. Use the provided `render.yaml` as a starting manifest for Render's Infrastructure as Code

After setting secrets, pushes to `main` or `version-2` will build images and (if configured) trigger Render deploys.

