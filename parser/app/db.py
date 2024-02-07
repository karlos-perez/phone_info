import logging
import sys

import psycopg2

logger = logging.getLogger(__name__)


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):  # noqa: WPS421
            cls._instance = super().__new__(cls)
        return cls._instance


class DB(Singleton):
    _db = 'dbname={name} user={user} password={pwd} host={host} port={port}'
    _table_name = 'phone_range'
    _connect = None

    def __init__(self, config):
        self._config = config

    def connection(self):
        db_address = self._db.format(
            name=self._config.db.db_name,
            user=self._config.db.db_user,
            pwd=self._config.db.db_pass,
            host=self._config.db.db_host,
            port=self._config.db.db_port,
        )
        try:
            self._connect = psycopg2.connect(db_address)  # noqa: WPS601
        except (Exception, psycopg2.DatabaseError) as err:
            logger.error(f'Error connect to Datbase: {err}')
            sys.exit(1)

    def disconnection(self):
        self._connect.close()

    def load_csv(self, file_name):
        with self._connect.cursor() as curr:
            with open(file_name, 'r') as fl:
                try:
                    curr.copy_from(
                        fl,
                        'phone_range',
                        columns=('id', 'phone_range', 'operator', 'region', 'inn', 'load_date'),
                        sep=';'
                    )
                except (Exception, psycopg2.DatabaseError) as err:
                    logger.error(err)
                    self._connect.rollback()
                    curr.close()
                    self.disconnection()
                else:
                    self._connect.commit()

    @property
    def last_id(self) -> int:
        sql = f"SELECT last_value FROM public.{self._table_name}_id_seq;"  # noqa: Q000, S608

        with self._connect.cursor() as curr:
            curr.execute(sql)
            return curr.fetchone()[0]

    def set_new_id(self):
        with self._connect.cursor() as curr:
            sql = f"SELECT setval(pg_get_serial_sequence('{self._table_name}', 'id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM {self._table_name};"  # noqa: E501, S608
            curr.execute(sql)
