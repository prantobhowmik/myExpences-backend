
from fastapi import Request
from starlette.responses import JSONResponse
from datetime import datetime, timedelta

def session_timeout_middleware(timeout_minutes=30):
    timeout = timedelta(minutes=timeout_minutes)
    async def middleware(request: Request, call_next):
        session_last = request.session.get('last_active', None)
        now = datetime.utcnow()
        if session_last:
            last_active = datetime.fromisoformat(session_last)
            if now - last_active > timeout:
                return JSONResponse({"detail": "Session expired. Please log in again."}, status_code=401)
        request.session['last_active'] = now.isoformat()
        response = await call_next(request)
        return response
    return middleware
