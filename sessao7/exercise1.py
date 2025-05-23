import logging

def configure_logging():
    """Configure the root logger with basic settings"""
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('application.log'),  
            logging.StreamHandler()                
        ]
    )

def log_messages():
    """Log messages at different severity levels"""
    logger = logging.getLogger()
    
    logger.debug("Debug message: This is for detailed diagnostic information")
    logger.info("Info message: Confirmation that things are working as expected")
    logger.warning("Warning message: Something unexpected happened, but the application continues")
    logger.error("Error message: Serious problem, the application couldn't perform some function")
    
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Exception message: Logging an exception with traceback")

if __name__ == "__main__":
    configure_logging()
    log_messages()
    print("Logging completed. Check application.log and console output.")