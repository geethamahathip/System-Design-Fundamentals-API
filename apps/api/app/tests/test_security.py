def test_protected_route_requires_auth(client):
    res = client.get("/links/1")
    assert res.status_code in [401, 403]


def test_idor_scoping(client):
    # user A
    a = client.post(
        "/links",
        json={"long_url": "https://a.com"},
        headers={"x-api-key": "key1"}
    ).json()

    # user B tries access (should fail or not find)
    res = client.get(
        f"/links/{a['id']}",
        headers={"x-api-key": "key2"}
    )

    assert res.status_code in [404, 403]