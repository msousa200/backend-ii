import logging
from logging.handlers import TimedRotatingFileHandler
import time

def configure_rotating_log():
    """Configure logging with daily rotation and detailed timestamps"""
    
    logging.basicConfig(handlers=[], level=logging.DEBUG)
    
    formatter = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d - %(levelname)-8s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = TimedRotatingFileHandler(
        'application.log',
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log_sample_messages():
    """Log messages at different levels"""
    logger = logging.getLogger()
    
    logger.debug("Detailed debug information")
    logger.info("System is operating normally")
    logger.warning("Non-critical issue detected")
    logger.error("Error in processing request")
    
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Critical math error occurred")
    
    time.sleep(0.1)  
    logger.info("Operation completed")

if __name__ == "__main__":
    configure_rotating_log()
    log_sample_messages()
    print("Enhanced logging completed. Check application.log* files")