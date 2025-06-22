import logging
import sys

def setup_logging(log_file='horrorbot.log'):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels DEBUG and above

    formatter = logging.Formatter(
        '%(asctime)s — %(name)s — %(levelname)s — %(message)s'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Show INFO and above in console
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Log everything DEBUG and above to file
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
