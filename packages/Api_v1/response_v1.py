from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime, timezone
from typing import Any, Optional

def api_out(
    *,
    success: bool = True,
    message: str = "",
    data: Any = None,
    errors: Optional[dict] = None,
    status: int = 200,
    meta: Optional[dict] = None,
    version: str = "v1"
) -> Response:
    
    now = datetime.now(timezone.utc).isoformat()

    # Build the structure directly
    content = {
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
        "meta": {
            "timestamp": now,
            "api_version": version,
            **(meta or {})
        }
    }

    # Return the DRF Response. 
    # The renderer will handle turning 'data' into JSON.
    return Response(content, status=status)