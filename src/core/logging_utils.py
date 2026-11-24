"""Structured JSON Logging Utility for Production Observability."""
from datetime import datetime, timezone
import json
import logging
from typing import Any, Dict


class JSONLogFormatter(logging.Formatter):
    """Formats log records as single-line structured JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            payload.update(record.extra_fields)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def log_structured_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    """Emits a structured JSON telemetry event."""
    payload = {"event": event, **fields}
    logger.info(json.dumps(payload, default=str))
