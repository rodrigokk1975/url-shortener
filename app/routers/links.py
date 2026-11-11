from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.link import LinkCreate, LinkResponse
from app.services.shortener import create_short_link

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
