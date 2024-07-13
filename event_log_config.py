import logging
from logging.handlers import RotatingFileHandler

# Configure logging
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_file = "app.log"

file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
