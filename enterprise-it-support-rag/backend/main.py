from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.config import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0",
              description="Local-first enterprise IT support RAG API")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list,
                   allow_credentials=False, allow_methods=["GET", "POST"],
                   allow_headers=["Content-Type", "X-API-Key"])
app.include_router(router)
