import pytest


def test_create_short_link_success(client):
    response = client.post("/links", json={"url": "https://www.google.com"})
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert len(data["short_code"]) == 6
    assert data["original_url"] == "https://www.google.com"
    assert data["short_url"].endswith(data["short_code"])
    assert "created_at" in data


@pytest.mark.parametrize(
    "invalid_url",
    [
        "javascript:alert(1)",
        "ftp://files.example.com",
        "file:///C:/secrets.txt",
        "htp://typo.com",
        "google.com",  # sem esquema
        "",  # vazio
        "   ",
        "http://",  # sem domínio
    ],
)
def test_create_short_link_invalid_url(client, invalid_url):
    response = client.post("/links", json={"url": invalid_url})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_create_short_link_reject_self_domain(client):
    # Tentativa de auto-encurtamento usando localhost:8000
    response = client.post("/links", json={"url": "http://localhost:8000/some-path"})
    assert response.status_code == 422
    data = response.json()
    assert any("próprio encurtador" in str(err) for err in data["detail"])
