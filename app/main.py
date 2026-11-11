from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas no banco de dados se não existirem
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para encurtamento de URLs e monitoramento de estatísticas de acesso.",
    lifespan=lifespan,
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Retorna o status de integridade da API."""
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}
