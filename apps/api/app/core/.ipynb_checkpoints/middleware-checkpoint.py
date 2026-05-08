import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")


class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()

        try:
            response = await call_next(request)

            latency_ms = round((time.time() - start) * 1000)

            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "route": request.url.path,
                    "status_code": response.status_code,
                    "latency_ms": latency_ms
                }
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Latency-MS"] = str(latency_ms)

            return response

        except Exception:
            latency_ms = round((time.time() - start) * 1000)

            logger.error(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "route": request.url.path,
                    "status_code": 500,
                    "latency_ms": latency_ms,
                    "error": "INTERNAL_SERVER_ERROR"
                }
            )

            raise