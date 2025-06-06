"""
JSON serializers for objects not serializable by default json code
"""

from datetime import datetime
from typing import Any


def datetime_json_serializer(obj: Any) -> str:
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
