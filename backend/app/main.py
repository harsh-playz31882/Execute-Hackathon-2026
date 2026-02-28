from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.routes_assets import router as assets_router
from .api.v1.routes_auth import router as auth_router
from .api.v1.routes_interests import router as interests_router
from .db.database import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="Renewable Energy Marketplace API", version="0.1.0")

    # Allow all origins during hackathon development. Restrict in production.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "ok"}

    # Versioned API routers
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(assets_router, prefix="/api/v1/assets", tags=["assets"])
    app.include_router(interests_router, prefix="/api/v1/interests", tags=["interests"])

    return app


app = create_app()

