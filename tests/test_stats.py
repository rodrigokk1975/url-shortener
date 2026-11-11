def test_link_stats_initial_state(client):
    # 1. Cria um link
    post_res = client.post("/links", json={"url": "https://python.org"})
    assert post_res.status_code == 201
    code = post_res.json()["short_code"]

    # 2. Consulta estatísticas imediatamente
    stats_res = client.get(f"/links/{code}/stats")
    assert stats_res.status_code == 200
    data = stats_res.json()
    assert data["short_code"] == code
    assert data["total_clicks"] == 0
    assert data["last_clicked_at"] is None
    assert "created_at" in data


def test_link_stats_increments_after_clicks(client):
    # 1. Cria um link
    post_res = client.post("/links", json={"url": "https://docs.pytest.org"})
    code = post_res.json()["short_code"]

    # 2. Simula 3 acessos/redirecionamentos
    for _ in range(3):
        redirect_res = client.get(f"/{code}", follow_redirects=False)
        assert redirect_res.status_code == 307

    # 3. Consulta as estatísticas
    stats_res = client.get(f"/links/{code}/stats")
    assert stats_res.status_code == 200
    data = stats_res.json()
    assert data["total_clicks"] == 3
    assert data["last_clicked_at"] is not None


def test_link_stats_not_found(client):
    response = client.get("/links/unknownCode99/stats")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "unknownCode99" in data["detail"]
