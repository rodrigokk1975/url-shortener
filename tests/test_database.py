from app.models.link import Link
from app.models.click import Click


def test_create_link_and_click_relationship(db_session):
    # 1. Cria um link
    link = Link(original_url="https://example.com/long-url", short_code="abc1234")
    db_session.add(link)
    db_session.commit()
    db_session.refresh(link)

    assert link.id is not None
    assert link.short_code == "abc1234"
    assert link.created_at is not None

    # 2. Registra um clique associado ao link
    click = Click(link_id=link.id)
    db_session.add(click)
    db_session.commit()
    db_session.refresh(click)

    assert click.id is not None
    assert click.link_id == link.id
    assert click.clicked_at is not None

    # 3. Verifica o relacionamento
    assert len(link.clicks) == 1
    assert link.clicks[0].id == click.id
    assert click.link.short_code == "abc1234"
