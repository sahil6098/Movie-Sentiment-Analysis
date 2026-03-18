# IMDb Sentiment Analysis

This project is a movie review sentiment analysis web application that predicts whether a review is positive or negative. It combines a FastAPI backend, a simple frontend, and a Hugging Face transformer model to give real-time sentiment predictions from user input.

The app is designed to be easy to run locally from VS Code terminal and simple to understand as an end-to-end NLP project. A user enters a review in the browser, the frontend sends it to the backend API, and the backend uses a pretrained transformer model to return the sentiment result.

## Project Overview

The project includes:

- a FastAPI backend for serving the API and frontend
- a static HTML, CSS, and JavaScript frontend
- a Hugging Face sentiment model: `distilbert-base-uncased-finetuned-sst-2-english`
- a notebook used for experimentation and model-related work

This makes the project useful both as:

- an NLP mini project
- a portfolio project for web + ML integration
- a base project that can be extended with confidence display, history, authentication, or deployment

## Features

- Analyze movie review sentiment in real time
- Predicts either `Positive` or `Negative`
- Returns a numeric prediction value for frontend logic
- Returns model confidence score from the Hugging Face pipeline
- Serves the frontend directly from the FastAPI app
- Includes a health endpoint for quick backend checks
- Supports running directly from VS Code terminal

## How It Works

1. The user types a movie review into the frontend form.
2. The frontend sends the review to `POST /api/predict`.
3. The FastAPI backend validates the request.
4. The backend loads the Hugging Face sentiment pipeline.
5. The model predicts the sentiment label and confidence score.
6. The API returns a JSON response to the frontend.
7. The frontend updates the UI with the final result.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Hugging Face Transformers
- PyTorch
- HTML
- CSS
- JavaScript

## Model Information

The backend uses:

- `distilbert-base-uncased-finetuned-sst-2-english`

This is a transformer-based sentiment analysis model available through Hugging Face. It is loaded through the `transformers.pipeline()` API and cached after the first call, which makes later predictions faster.

## Project Structure

- `backend/app.py` contains the FastAPI application and prediction logic
- `backend/requirements.txt` contains backend dependencies
- `frontend/index.html` contains the page structure
- `frontend/style.css` contains the UI styling
- `frontend/app.js` handles browser-side form submission and UI updates
- `notebooks/SentimentAnalysis.ipynb` contains the notebook work
- `start.bat` starts the app using the local virtual environment

## Setup

Open VS Code terminal in the project folder:

```powershell
cd "F:\Sahil\SentimentAnalysis"
```

If needed, activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Install dependencies:

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

Then open this URL in your browser:

```text
http://127.0.0.1:8000/
```

## API Endpoints

- `GET /` serves the frontend
- `GET /health` returns backend status
- `POST /api/predict` predicts sentiment from review text

## Example Request

```json
{
  "review": "This movie was amazing, emotional, and beautifully acted."
}
```

## Example Response

```json
{
  "sentiment": "Positive",
  "prediction": 1,
  "score": 0.9998,
  "model": "distilbert-base-uncased-finetuned-sst-2-english"
}
```

## Notes

- The first prediction can take longer because the model is loaded on first use.
- If the model is not cached, Hugging Face may download it during the first run.
- If port `8000` is already in use, stop the other process or run on another port:

```powershell
$env:PORT="8001"
python .\backend\app.py
```

## Future Improvements

- Show confidence score in the frontend
- Add sentiment history
- Add batch prediction support
- Deploy the app to Render, Railway, or Hugging Face Spaces
- Add tests for API endpoints and prediction flow
