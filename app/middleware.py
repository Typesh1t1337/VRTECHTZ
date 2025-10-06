from time import time
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json
import logging


logger = logging.getLogger(__name__)


class JSONLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, log_request: bool = False):
        super().__init__(app)
        self.log_request = log_request

    async def dispatch(self, request: Request, call_next):
        start_time = time()
        body = None
        if self.log_request:
            try:
                body_bytes = await request.body()
                body = json.loads(body_bytes.decode('utf-8'))
            except Exception:
                body = None

        logger.info({
            "event": "request",
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host if request.client else None,
            "body": body,
        })

        try:
            response: Response = await call_next(request)
            process_time = round(time() - start_time, 3)

            logger.info({
                "event": "response",
                "status_code": response.status_code,
                "method": request.method,
                "url": str(request.url),
                "duration": process_time,
            })
            return response
        except Exception as e:
            logger.error({
                "event": "error",
                "method": request.method,
                "url": str(request.url),
                "error": str(e),
            })
            raise

