import os
import time
import logging
from fastapi import Request
from starlette.routing import Match
from starlette.middleware.base import BaseHTTPMiddleware

if os.getenv('LOGS', 'console') == 'file':
    logging.config.fileConfig("config/file.conf")
else:
    logging.config.fileConfig('config/console.conf')
    
logger = logging.getLogger("appLogger")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        name = ""
        for route in request.app.routes:
            if hasattr(route, "endpoint"):
                match, scope = route.matches(request.scope)
                if match == Match.FULL:
                    name = str(route.endpoint.__name__).replace("_", " ").title()
                    break  # Exit the loop once a match is found

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        if name != "":
            logger.info(f"API | {name} | {duration:.3f}s")
        return response
