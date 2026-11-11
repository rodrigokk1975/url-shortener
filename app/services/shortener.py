import secrets
import string
from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.link import Link
from app.models.click import Click

CHARS = string.ascii_letters + string.digits  # a-z, A-Z, 0-9 (base62)
CODE_LENGTH = 6
MAX_ATTEMPTS = 10


def generate_random_code(length: int = CODE_LENGTH) -> str:
    """Gera um código alfanumérico seguro com o comprimento especificado."""
    return "".join(secrets.choice(CHARS) for _ in range(length))


def get_link_by_code(db: Session, code: str) -> Link | None:
    """Busca um link pelo código curto."""
    return db.query(Link).filter(Link.short_code == code).first()


def create_short_link(db: Session, original_url: str) -> Link:
    """Gera um código único e cria o registro de encurtamento no banco."""
    for _ in range(MAX_ATTEMPTS):
        code = generate_random_code()
        # Garante unicidade verificando se já existe
        if not get_link_by_code(db, code):
            link = Link(original_url=original_url, short_code=code)
            db.add(link)
            db.commit()
            db.refresh(link)
            return link

    raise RuntimeError("Não foi possível gerar um código único após várias tentativas.")


def record_click(db: Session, link_id: int) -> Click:
    """Registra um evento de clique para o link especificado com data e hora UTC."""
    click = Click(link_id=link_id, clicked_at=datetime.now(timezone.utc))
    db.add(click)
    db.commit()
    db.refresh(click)
    return click


def get_link_stats(db: Session, link: Link) -> dict:
    """Calcula estatísticas de acesso de um link."""
    total_clicks = db.query(func.count(Click.id)).filter(Click.link_id == link.id).scalar() or 0
    last_clicked_at = db.query(func.max(Click.clicked_at)).filter(Click.link_id == link.id).scalar()

    return {
        "total_clicks": total_clicks,
        "last_clicked_at": last_clicked_at,
    }
