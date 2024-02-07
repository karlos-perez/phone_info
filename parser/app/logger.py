import logging
import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

LEVEL = {  # noqa: WPS407
    'noset': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'fatal': logging.FATAL,
    'critical': logging.CRITICAL,
}


def setup_logging(config) -> None:
    path_log_file = os.path.join(BASE_DIR, 'deploy/logs/parser.log')
    file_log = logging.FileHandler(path_log_file)
    console_out = logging.StreamHandler()
    logging.basicConfig(
        handlers=(file_log, console_out),
        format='[%(asctime)s | %(levelname)s]: %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
        level=LEVEL[config.logger.level],
    )
