def test_create_link(client):
    res = client.put(
        "/links/1",
        headers={"X-API-Key": "key1"},
        json={"long_url": "https://google.com"}
    )

    assert res.status_code == 200
    assert "code" in res.json()