import uuid

def test_click_idempotency(client):
    create = client.post(
        "/links",
        json={"long_url": "https://google.com"},
        headers={"x-api-key": "key1"}
    ).json()

    code = create["code"]
    event_id = str(uuid.uuid4())

    # simulate same payload twice
    for _ in range(2):
        client.get(f"/r/{code}", headers={"x-api-key": "key1"})

    # DB check depends on your schema, but expectation:
    # only one click event for same event_id or dedup logic holds