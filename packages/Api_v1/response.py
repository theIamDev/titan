from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime, timezone
from typing import Any, Optional

# check for decom
# --- Response Serializer Definitions ---

class ResponseEnvelopeSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = serializers.JSONField(allow_null=True)
    errors = serializers.JSONField(allow_null=True)
    meta = serializers.JSONField(allow_null=True)


# --- Response Builder ---

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
    """
    Standardized DRF response builder with serialization + schema enforcement.
    """
    now = datetime.now(timezone.utc).isoformat()

    meta_block = {
        "timestamp": now,
        "api_version": version,
        **(meta or {})
    }

    envelope = {
        "success": success,
        "message": message,
        "data": data if success else None,
        "errors": errors if not success else None,
        "meta": meta_block
    }

    serializer = ResponseEnvelopeSerializer(data=envelope)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status)
