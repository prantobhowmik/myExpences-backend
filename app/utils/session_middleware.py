from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timedelta

class SessionTimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout_minutes=30):
        super().__init__(app)
        self.timeout = timedelta(minutes=timeout_minutes)

    async def dispatch(self, request: Request, call_next):
        session_last = request.session.get('last_active') if hasattr(request, 'session') else None
        now = datetime.utcnow()
        if session_last:
            last_active = datetime.fromisoformat(session_last)
            if now - last_active > self.timeout:
                return JSONResponse({"detail": "Session expired. Please log in again."}, status_code=401)
        # Update session last active
        if hasattr(request, 'session'):
            request.session['last_active'] = now.isoformat()
        response = await call_next(request)
        return response
