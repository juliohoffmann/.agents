import logging
from src.utils.config import Config

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        fh = logging.FileHandler(Config.LOG_FILE, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger