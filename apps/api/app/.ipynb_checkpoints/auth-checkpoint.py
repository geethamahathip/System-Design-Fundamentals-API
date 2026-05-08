from fastapi import Header, HTTPException

API_KEYS = {
    "key1": "t1",
    "key2": "t2",
}

def get_principal(x_api_key: str = Header(None)) -> str:
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return API_KEYS[x_api_key]