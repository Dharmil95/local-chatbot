import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.msg = (
            f"{record.lineno}:{record.funcName} ({record.filename}): {record.msg}"
        )
        return super().format(record)


def setup_logger():
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(CustomFormatter())
        logger.addHandler(stream_handler)
    return logger
