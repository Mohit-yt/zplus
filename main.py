from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

from .routes import preharvest, market, profit, recommendation, risk


BASE_DIR = Path(__file__).resolve().parent.parent


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Vriksh 2.0 Backend",
        description="FastAPI backend bridging Vriksh 1 pre-harvest model, Pathway outputs, and the frontend dashboard.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(preharvest.router, prefix="", tags=["Pre-Harvest Prediction"])
    app.include_router(market.router, prefix="", tags=["Market Prices"])
    app.include_router(profit.router, prefix="", tags=["Profit"])
    app.include_router(recommendation.router, prefix="", tags=["Recommendations"])
    app.include_router(risk.router, prefix="", tags=["Risk"])

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        return {"status": "ok"}

    return app


app = create_app()

