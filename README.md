# IMDb Sentiment Analysis

This project is a movie-review sentiment analysis web app built with:

- FastAPI for the backend API
- a static HTML/CSS/JavaScript frontend
- a Hugging Face sentiment model: `distilbert-base-uncased-finetuned-sst-2-english`

## Project Structure

- `backend/app.py` runs the FastAPI server and prediction API
- `backend/requirements.txt` contains backend dependencies
- `frontend/` contains the user interface
- `start.bat` starts the project with the local virtual environment

## Setup

Open VS Code terminal at:

```powershell
cd "PROJECT FOLDER"
```

If needed, activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Install the backend dependencies:

```powershell
pip install -r .\backend\requirements.txt
```

## Run The Project

Option 1:

```powershell
python .\backend\app.py
```

Option 2:

```powershell
python -m uvicorn backend.app:app --reload
```

Option 3:

```powershell
.\start.bat
```

Then open:

```text
http://127.0.0.1:8000/
```

## API Endpoints

- `GET /` serves the frontend
- `GET /health` returns backend status
- `POST /api/predict` predicts sentiment from the submitted review

## Notes

- The first prediction can take longer because the Hugging Face model is loaded on first use.
- If port `8000` is already in use, stop the old process or run on another port:

```powershell
$env:PORT="8001"
python .\backend\app.py
```
