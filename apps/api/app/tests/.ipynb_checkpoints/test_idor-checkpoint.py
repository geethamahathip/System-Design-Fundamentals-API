def test_idor_prevention(client):
    res1 = client.put(
        "/links/1",
        headers={"X-API-Key": "key1"},
        json={"long_url": "https://a.com"}
    )

    res2 = client.put(
        "/links/1",
        headers={"X-API-Key": "key2"},
        json={"long_url": "https://b.com"}
    )

    assert res2.status_code in (403, 404)