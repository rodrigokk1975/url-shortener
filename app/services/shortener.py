import secrets
import string
from sqlalchemy.orm import Session
from app.models.link import Link

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
