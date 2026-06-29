from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import chat_routes, diagnostic_routes, rag_routes, study_plan_routes, topic_routes

app = FastAPI(title=settings.app_name, docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

_prefix = settings.api_prefix
app.include_router(chat_routes.router, prefix=_prefix)
app.include_router(topic_routes.router, prefix=_prefix)
app.include_router(rag_routes.router, prefix=_prefix)
app.include_router(diagnostic_routes.router, prefix=_prefix)
app.include_router(study_plan_routes.router, prefix=_prefix)


@app.get(f"{_prefix}/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}
