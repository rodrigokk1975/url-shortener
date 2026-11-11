from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.shortener import get_link_by_code

router = APIRouter(tags=["Redirection"])


@router.get(
    "/{code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="Redirecionar para URL original",
    description="Redireciona o cliente para a URL original com status HTTP 307 (Temporary Redirect).",
)
def redirect_to_original(
    code: str,
    db: Session = Depends(get_db),
):
    link = get_link_by_code(db, code)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link com o código '{code}' não foi encontrado.",
        )

    return RedirectResponse(
        url=link.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
