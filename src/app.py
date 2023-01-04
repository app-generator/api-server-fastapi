from fastapi import FastAPI
from src.config import settings


if (settings.debugging):
    app = FastAPI(debug=True, reload=True, port=5000)
else:
    app = FastAPI(port=5000)
