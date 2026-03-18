import os
import socket
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"
MODEL_NAME = os.getenv(
    "HF_SENTIMENT_MODEL",
    "distilbert-base-uncased-finetuned-sst-2-english",
)


@lru_cache
def get_sentiment_pipeline():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: install backend requirements to use the Hugging Face model."
        ) from exc

    try:
        return pipeline("sentiment-analysis", model=MODEL_NAME)
    except Exception as exc:
        raise RuntimeError(
            f"Unable to load Hugging Face model '{MODEL_NAME}'. "
            "Make sure dependencies are installed and the model can be downloaded or is cached locally."
        ) from exc


app = FastAPI(
    title="IMDb Sentiment Analysis API",
    description="Predicts whether a movie review is positive or negative.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class ReviewRequest(BaseModel):
    review: str = Field(..., min_length=1, description="Movie review text")


class PredictionResponse(BaseModel):
    sentiment: str
    prediction: int
    score: float
    model: str


@app.get("/health")
def health_check():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/api/predict", response_model=PredictionResponse)
def predict_sentiment(payload: ReviewRequest):
    review = payload.review.strip()
    if not review:
        raise HTTPException(status_code=400, detail="Review cannot be empty.")

    try:
        classifier = get_sentiment_pipeline()
        result = classifier(review)[0]
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The sentiment model failed while processing the review.",
        ) from exc

    label = str(result.get("label", "")).upper()
    score = float(result.get("score", 0.0))
    is_positive = label == "POSITIVE"

    return {
        "sentiment": "Positive" if is_positive else "Negative",
        "prediction": 1 if is_positive else 0,
        "score": score,
        "model": MODEL_NAME,
    }


@app.get("/")
def serve_homepage():
    index_file = FRONTEND_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend files not found.")
    return FileResponse(index_file)


def ensure_port_available(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError as exc:
            raise SystemExit(
                f"Port {port} is already in use on {host}. "
                f"Close the other server or run with a different port, for example: "
                f"$env:PORT='{port + 1}'; python .\\backend\\app.py"
            ) from exc


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    ensure_port_available(host, port)
    uvicorn.run(app, host=host, port=port)
