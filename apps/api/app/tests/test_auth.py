def test_protected_route_requires_auth(client):
    res = client.put(
        "/links/1",
        json={"long_url": "https://google.com"}
    )

    assert res.status_code == 401