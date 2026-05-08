def test_retention_purge(client):
    res = client.post("/admin/purge-clicks?days=0")
    assert res.status_code in (200, 204)