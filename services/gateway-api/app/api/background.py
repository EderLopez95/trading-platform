import logging
from app.infrastructure.grpc.clients.providers import get_signal_client

logger = logging.getLogger("gateway")

def refresh_registries_safe():
    try:
        get_signal_client().refresh_registries()

    except Exception as e:
        logger.error(
            "refresh_registries_failed",
            extra={
                "error": str(e),
            }
        )
