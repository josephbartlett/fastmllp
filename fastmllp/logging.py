import logging as std_logging

LEVELS = {
    "debug": std_logging.DEBUG,
    "info": std_logging.INFO,
    "warning": std_logging.WARNING,
    "error": std_logging.ERROR,
}


def resolve_level(level: str) -> int:
    return LEVELS.get(level.lower(), std_logging.INFO)


def configure_logging(level: str = "info") -> std_logging.Logger:
    logger = std_logging.getLogger("fastmllp")
    if not logger.handlers:
        handler = std_logging.StreamHandler()
        formatter = std_logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel(resolve_level(level))
    return logger


def log_event(
    logger: std_logging.Logger,
    level: int,
    event: str,
    conn_id: int | None = None,
    **fields: object,
) -> None:
    parts = [f"event={event}"]
    if conn_id is not None:
        parts.append(f"conn_id={conn_id}")
    for key, value in fields.items():
        parts.append(f"{key}={value}")
    logger.log(level, " ".join(parts))
