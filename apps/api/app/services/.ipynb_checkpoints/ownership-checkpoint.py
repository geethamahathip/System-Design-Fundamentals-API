from fastapi import HTTPException


def assert_ownership(db_value, tenant_id):
    if db_value != tenant_id:
        raise HTTPException(status_code=404, detail="Not found")