import hashlib
def hash_ip(ip: str) -> str:
    if not ip:
        return "unknown"
    return hashlib.sha256(ip.encode()).hexdigest()