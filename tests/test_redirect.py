def test_redirect_to_original_url_success(client):
    # 1. Cria um link curto
    post_res = client.post("/links", json={"url": "https://fastapi.tiangolo.com"})
    assert post_res.status_code == 201
    code = post_res.json()["short_code"]

    # 2. Acessa a rota /{code} sem seguir automaticamente o redirect
    get_res = client.get(f"/{code}", follow_redirects=False)
    assert get_res.status_code == 307
    assert get_res.headers["location"] == "https://fastapi.tiangolo.com"


def test_redirect_code_not_found(client):
    # Acessa código aleatório inexistente
    response = client.get("/nonexistent123", follow_redirects=False)
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "nonexistent123" in data["detail"]
