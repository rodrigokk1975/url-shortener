from datetime import datetime
from urllib.parse import urlparse
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.core.config import settings


class LinkCreate(BaseModel):
    url: str = Field(
        ...,
        description="URL de destino a ser encurtada (apenas http ou https).",
        examples=["https://www.google.com"],
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        clean_url = v.strip()
        if not clean_url:
            raise ValueError("A URL não pode estar vazia.")

        parsed = urlparse(clean_url)
        if parsed.scheme.lower() not in ("http", "https"):
            raise ValueError("A URL deve iniciar obrigatoriamente com o protocolo http:// ou https://.")

        if not parsed.netloc:
            raise ValueError("A URL informada não possui um domínio válido.")

        # Prevenção contra auto-encurtamento (loop)
        base_host = urlparse(settings.BASE_URL).netloc
        if parsed.netloc.lower() == base_host.lower():
            raise ValueError("Não é permitido encurtar uma URL do próprio encurtador.")

        return clean_url


class LinkResponse(BaseModel):
    id: int
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LinkStatsResponse(BaseModel):
    id: int
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime
    total_clicks: int
    last_clicked_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
