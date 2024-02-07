import csv
import logging
from datetime import date

logger = logging.getLogger(__name__)


class DataProcessing:
    def transform_data(
        self, source_file: str, processed_file: str, last_id: int,
    ) -> None:
        """
        Preparation data and save new csv for loading into the database

        :param source_file:
        :param processed_file:
        :param last_id: Last id in
        """
        with open(source_file, 'r') as fl_source:
            with open(processed_file, 'w') as fl_result:
                raw_data = csv.reader(fl_source, delimiter=';')
                result_csv = csv.writer(
                    fl_result, delimiter=';', quotechar="'", quoting=csv.QUOTE_MINIMAL,
                )

                next(raw_data)

                for row in raw_data:
                    end_range = f'{row[0]}{row[2]:0>7}'
                    number_range = f'[{row[0]}{row[1]:0>7},{int(end_range) + 1})'  # noqa: WPS221, WPS237
                    last_id += 1

                    result_csv.writerow(
                        (
                            last_id,
                            number_range,
                            row[4] if row[4] else '',
                            row[5] if row[5] else '',
                            int(row[6]) if row[6] else 0,
                            date.today(),
                        ),
                    )
