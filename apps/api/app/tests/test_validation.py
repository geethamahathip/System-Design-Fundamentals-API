def test_invalid_url_rejected(client):
    res = client.put(
        "/links/1",
        headers={"X-API-Key": "key1"},
        json={"long_url": "javascript:alert(1)"}
    )

    assert res.status_code == 400