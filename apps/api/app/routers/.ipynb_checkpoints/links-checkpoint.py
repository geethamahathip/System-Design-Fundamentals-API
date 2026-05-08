from fastapi import APIRouter, Depends, HTTPException, Request, Query, Header
from sqlalchemy import or_
from sqlalchemy.orm import Session
import uuid
import time
from app.schemas.link import CreateLinkRequest
from app.services.links_service import create_link
from app.auth import get_principal
from app.db import SessionLocal
from app.models.link import Link
from app.rate_limiter import check_rate_limit
import app.config as config
from app.cache.redis_client import delete_redirect
from datetime import datetime, timedelta
from app.models.click_event import ClickEvent
import re
router = APIRouter()
#create link
@router.post("/links")
def create_link_route(
    payload: CreateLinkRequest,
    request: Request,
    principal: str = Depends(get_principal),
):
    check_rate_limit(principal, limit=30)
    link = create_link(payload, principal)
    return {
        "id": link.id,
        "code": link.code,
        "long_url": link.long_url,
        "short_url": f"/r/{link.code}",
        "created_at": link.created_at,
        "expires_at": link.expires_at,
    }
MAX_PAGE_SIZE = 50
ALLOWED_SORT_FIELDS = {"created_at", "click_count"}
@router.get("/links/search")
def search_links(
    q: str = "",
    tag: str = "",
    page: int = 1,
    page_size: int = 20,
    sort: str = Query("created_at"), 
    x_api_key: str = Header(None, alias="x-api-key")
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    if sort not in ALLOWED_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Allowed: {sorted(ALLOWED_SORT_FIELDS)}"
        )
    if page < 1:
        page = 1
    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE
    db = SessionLocal()
    try:
        query = db.query(Link).filter(Link.tenant_id == "t1")
        if q:
            query = query.filter(
                or_(
                    Link.code.ilike(f"%{q}%"),
                    Link.long_url.ilike(f"%{q}%")
                )
            )
        if tag:
            query = query.filter(Link.tag == tag)
        # (optional future hook — no execution yet)
        if sort == "created_at":
            query = query.order_by(Link.created_at.desc())
        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        return {
            "items": [
                {
                    "id": i.id,
                    "code": i.code,
                    "long_url": i.long_url,
                    "created_at": i.created_at
                }
                for i in items
            ],
            "page": page,
            "page_size": page_size,
            "total": total
        }
    finally:
        db.close()
#get link
@router.get("/links/{link_id}")
def get_link(link_id: int, principal: str = Depends(get_principal)):
    db = SessionLocal()
    try:
        if config.FORCE_DB_ERROR:
            raise Exception("Simulated DB failure")
        link = db.query(Link).filter(
            Link.id == link_id,
            Link.tenant_id == principal
        ).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return {
            "id": link.id,
            "code": link.code,
            "long_url": link.long_url,
        }
    finally:
        db.close()
#delete link
@router.delete("/links/{link_id}")
def delete_link(link_id: int, request: Request, principal: str = Depends(get_principal)):
    request_id = getattr(request.state, "request_id", None)
    db = SessionLocal()
    try:
        link = db.query(Link).filter(
            Link.id == link_id,
            Link.tenant_id == principal
        ).first()
        if not link:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": {
                        "code": "NOT_FOUND",
                        "message": "Link not found",
                        "request_id": request_id,
                    }
                },
            )
        code = link.code
        db.delete(link)
        db.commit()
        try:
            delete_redirect(code)
            print("CACHE_INVALIDATED_DELETE:", code)
        except Exception as e:
            print("DELETE_FAILED:", e)
        return {"message": "Deleted"}
    finally:
        db.close()
#update link
@router.put("/links/{link_id}")
def update_link(
    link_id: int,
    payload: dict,
    request: Request,
    principal: str = Depends(get_principal),
):
    request_id = getattr(request.state, "request_id", None)
    db = SessionLocal()
    try:
        link = db.query(Link).filter(
            Link.id == link_id,
            Link.tenant_id == principal
        ).first()
        if not link:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": {
                        "code": "NOT_FOUND",
                        "message": "Link not found",
                        "request_id": request_id,
                    }
                },
            )
        new_url = payload.get("long_url")
        
        if new_url:
            if not re.match(r"^https?://", new_url):
                raise HTTPException(status_code=400, detail="Invalid URL")
            link.long_url = new_url
        db.commit()
        db.refresh(link)
        try:
            delete_redirect(link.code)
            print("CACHE_INVALIDATED:", link.code)
        except Exception as e:
            print("DELETE_FAILED:", e)
        return {
            "id": link.id,
            "code": link.code,
            "long_url": link.long_url,
            "short_url": f"/r/{link.code}",
            "created_at": link.created_at,
            "expires_at": link.expires_at,
        }
    finally:
        db.close()
@router.post("/admin/purge-clicks")
def purge_clicks(days: int = 30):
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)

        deleted = (
            db.query(ClickEvent)
            .filter(ClickEvent.timestamp < cutoff)
            .delete()
        )

        db.commit()
        return {"deleted": deleted}
    finally:
        db.close()