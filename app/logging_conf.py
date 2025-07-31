import logging
import structlog
from .config import get_settings

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(message)s",
    handlers=[logging.StreamHandler()],
)

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(settings.log_level)),
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)
logger = structlog.get_logger()
