import pathlib
from dataclasses import dataclass

import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent


@dataclass
class LoggingConfig:
    level: str = ''


@dataclass
class LoaderConfig:
    target_url: str = ''
    path_new_files: str = f'{BASE_DIR}/csv'
    path_old_files: str = f'{BASE_DIR}/csv/old'


@dataclass
class DBConfig:
    db_name: str = None
    db_user: str = f'{BASE_DIR}/csv'
    db_pass: str = f'{BASE_DIR}/csv/old'
    db_host: str = f'{BASE_DIR}/csv/old'
    db_port: str = f'{BASE_DIR}/csv/old'


@dataclass
class Config:
    logger: 'LoggingConfig'
    loader: 'LoaderConfig'
    db: 'DBConfig'


def get_config(path=None):
    if path is None:
        path = f'{BASE_DIR}/config.yml'

    with open(path) as fl:
        parsed_config = yaml.safe_load(fl)
    return parsed_config


def setup_config():
    raw_config = get_config()
    db_config = raw_config['db']
    return Config(
        logger=LoggingConfig(
            level=raw_config['logger']['level'],
        ),
        loader=LoaderConfig(
            target_url=raw_config['loader']['target'],
        ),
        db=DBConfig(
            db_name=db_config['dbname'],
            db_user=db_config['user'],
            db_pass=db_config['password'],
            db_host=db_config['host'],
            db_port=db_config['port'],
        ),
    )
