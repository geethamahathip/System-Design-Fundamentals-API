import logging
class RedactFilter(logging.Filter):
    def filter(self, record):
        msg = str(record.getMessage())
        # redact API keys
        msg = msg.replace("X-API-Key", "***REDACTED***")
        msg = msg.replace("DO_NOT_LOG_ME_123", "***REDACTED***")
        record.msg = msg
        return True
def setup_logging():
    logger = logging.getLogger("app")
    logger.addFilter(RedactFilter())