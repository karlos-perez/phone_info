import filecmp
import logging
import os
from parser.app.db import DB
from parser.app.processing import DataProcessing

logger = logging.getLogger(__name__)


class UploaderToDB:
    def __init__(self, config):
        self._config = config

        self._path_new_files = config.loader.path_new_files
        self._path_old_files = config.loader.path_old_files
        self._db = DB(config)
        self._processing = DataProcessing()

    def upload(self, files_name: list[str]):
        files_to_upload = []

        for file_name in files_name:
            if not self._comparison_files(file_name):
                files_to_upload.append(file_name)

        if not files_to_upload:
            logger.info('No change in files')
            return

        self._db.connection()
        self._db.set_new_id()

        for file_name in files_to_upload:  # noqa: WPS440
            source_file = os.path.join(self._path_new_files, file_name)
            processed_file = os.path.join(self._path_new_files, f'load_{file_name}')
            last_id = self._db.last_id

            self._processing.transform_data(source_file, processed_file, last_id)
            self._db.load_csv(processed_file)
            self._db.set_new_id()

            os.remove(processed_file)

            logger.info(f'File: {file_name} upload to DB')

        self._db.disconnection()

    def _comparison_files(self, file_name: str) -> bool:
        """Comparison old and new CSV files

        :param file_name:
        """
        old_file = os.path.join(self._path_old_files, file_name)
        new_file = os.path.join(self._path_new_files, file_name)

        if os.path.exists(old_file):
            return filecmp.cmp(old_file, new_file)

        return False
