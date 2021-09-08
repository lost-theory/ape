import logging
import sys

import click
import click_logging

CLICK_STYLE_KWARGS = {
    "EXCEPTION": dict(fg="red"),
    "CRITICAL": dict(fg="red"),
    "ERROR": dict(fg="red"),
    "WARNING": dict(fg="yellow"),
    "INFO": dict(),
    "DEBUG": dict(fg="blue"),
}


class ApeColorFormatter(logging.Formatter):
    def format(self, record):
        if click._compat.isatty(sys.stdout) and click._compat.isatty(sys.stderr):
            # only color log messages when sys.stdout and sys.stderr are sent to the terminal
            record.levelname = click.style(record.levelname, **CLICK_STYLE_KWARGS[record.levelname])
        return super().format(record)


def get_logger(name) -> logging.Logger:
    """Get a logger with the given ``name`` and configure it for usage with Click."""
    logger = logging.getLogger(name)
    click_logging.basic_config(logger)
    handler = logging.StreamHandler()
    handler.setFormatter(
        ApeColorFormatter(
            "[%(asctime)s] %(levelname)s [%(name)s:%(module)s:%(lineno)s]: %(message)s"
        )
    )
    logger.handlers = [handler]

    return logger


logger = get_logger("ape")
