# movie_recommender_system

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
