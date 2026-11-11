from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para encurtamento de URLs e monitoramento de estatísticas de acesso.",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Retorna o status de integridade da API."""
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}
