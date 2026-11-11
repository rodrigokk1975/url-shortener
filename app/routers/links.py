from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.link import LinkCreate, LinkResponse, LinkStatsResponse
from app.services.shortener import (
    create_short_link,
    get_link_by_code,
    get_link_stats,
)

router = APIRouter(prefix="/links", tags=["Links"])


@router.post(
    "",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar link curto",
    description="Recebe uma URL longa e retorna o código curto único gerado.",
)
def create_link_endpoint(
    payload: LinkCreate,
    db: Session = Depends(get_db),
) -> dict:
    link = create_short_link(db, original_url=payload.url)
    return {
        "id": link.id,
        "short_code": link.short_code,
        "original_url": link.original_url,
        "short_url": f"{settings.BASE_URL.rstrip('/')}/{link.short_code}",
        "created_at": link.created_at,
    }


@router.get(
    "/{code}/stats",
    response_model=LinkStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar estatísticas do link",
    description="Retorna métricas de acesso do link encurtado, incluindo total de cliques e último acesso.",
)
def get_link_stats_endpoint(
    code: str,
    db: Session = Depends(get_db),
) -> dict:
    link = get_link_by_code(db, code)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link com o código '{code}' não foi encontrado.",
        )

    stats = get_link_stats(db, link)
    return {
        "id": link.id,
        "short_code": link.short_code,
        "original_url": link.original_url,
        "short_url": f"{settings.BASE_URL.rstrip('/')}/{link.short_code}",
        "created_at": link.created_at,
        "total_clicks": stats["total_clicks"],
        "last_clicked_at": stats["last_clicked_at"],
    }
