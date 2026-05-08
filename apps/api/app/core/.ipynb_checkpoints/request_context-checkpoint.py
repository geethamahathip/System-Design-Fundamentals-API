from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default=None)

def set_request_id(rid: str):
    request_id_ctx.set(rid)

def get_request_id():
    return request_id_ctx.get()