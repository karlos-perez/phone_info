import logging
import os
import shutil

import httpx

logger = logging.getLogger(__name__)


class FilesLoader:
    _headers = {
        'User': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',  # noqa: E501
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, * / *;q = 0.8',  # noqa: E501
        'Accept-Language': 'ru, en - US; q = 0.7, en; q = 0.3',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    _url_files = []
    _name_files = []

    def __init__(self, config, parser):
        self._url = config.loader.target_url
        self._parser = parser()
        self._path_new_files = config.loader.path_new_files
        self._path_old_files = config.loader.path_old_files

    def get_files(self) -> list[str]:
        """Download csv files

        :return:
        """
        response = httpx.get(self._url, headers=self._headers, verify=False)  # noqa: S501

        if response.status_code == 200:
            for url in self._parser.get_files_links(response.text):
                self._download(url)
        else:
            logger.error(f'{response.status_code}: {response.text}')

        return self._name_files

    def _download(self, url: str) -> None:
        """Download file and write to disk

        :param url:
        :return:
        """

        file_name = self._make_filename(url)

        self._move_old_files(file_name)

        path = os.path.join(self._path_new_files, file_name)

        with open(path, 'wb') as download_file:
            with httpx.stream(
                'GET', url, headers=self._headers, verify=False,  # noqa: S501
            ) as response:
                for chunk in response.iter_bytes():
                    download_file.write(chunk)

        self._name_files.append(file_name)

    def _make_filename(self, url: str) -> str:
        """Gets file name from url
        :param url:
        :return:
        """
        return url.split('/')[-1].split('?')[0]

    def _move_old_files(self, file_name: str) -> None:
        """Move old file in archive

        :param file_name:
        """
        old_file = os.path.join(self._path_old_files, file_name)

        if os.path.exists(old_file):
            os.remove(old_file)

        new_file = os.path.join(self._path_new_files, file_name)

        if os.path.exists(new_file):
            shutil.move(new_file, self._path_old_files)
