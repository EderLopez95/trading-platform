import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s "
        "%(request_id)s %(user_id)s %(method)s %(path)s "
        "%(status_code)s %(duration_ms)s %(client_ip)s %(error)s",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level",
        },
    )

    handler.setFormatter(formatter)
    logger.handlers = [handler]
