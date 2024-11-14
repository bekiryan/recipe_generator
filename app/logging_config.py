import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

file_handler = RotatingFileHandler("logs/app.log", maxBytes=10**6, backupCount=5)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
