import logging
from parser.app.config import setup_config
from parser.app.files_loader import FilesLoader
from parser.app.logger import setup_logging
from parser.app.parser_page import ParserPage
from parser.app.upload_db import UploaderToDB

logger = logging.getLogger(__name__)


def run_app():
    config = setup_config()
    setup_logging(config)
    files_name = FilesLoader(config, ParserPage).get_files()

    if files_name:
        uploader = UploaderToDB(config)
        uploader.upload(files_name)


if __name__ == '__main__':
    run_app()
