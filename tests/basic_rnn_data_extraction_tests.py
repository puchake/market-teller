import unittest
from collections import namedtuple
import csv
import pickle
import numpy as np

import src.basic_nn.data_extraction as data_extraction


# Input and output files paths relative to this tests file.
RAW_DATA_FILE_PATH = "../data/raw/wiki_prices_data.csv"
EXTRACTED_DATA_FILE_PATH = "../data/extracted/wiki_prices_data.npy"
COMPANIES_DICT_FILE_PATH = "../data/extracted/companies_dict.pickle"


class BasicRnnDataExtractionTestCase(unittest.TestCase):

    def test_extracted_wiki_prices_data_number_of_rows(self):

        # Arrange
        csv_file = open(RAW_DATA_FILE_PATH)
        csv_reader = csv.reader(csv_file)
        data_matrix = np.load(EXTRACTED_DATA_FILE_PATH)

        # Skip header row.
        next(csv_reader)

        # Act
        csv_row_count = sum(1 for row in csv_reader)

        # Assert
        self.assertEqual(csv_row_count, data_matrix.shape[0])

    def test_extracted_wiki_prices_data_numeric_values(self):

        # Arrange
        csv_file = open(RAW_DATA_FILE_PATH)
        csv_reader = csv.reader(csv_file)
        data_matrix = np.load(EXTRACTED_DATA_FILE_PATH)
        CsvRow = namedtuple("CsvRow", data_extraction.CSV_ROW_FIELDS)
        results = np.empty([data_matrix.shape[0], ], dtype=np.bool)

        # Skip header row.
        next(csv_reader)

        # Act
        for row, i in zip(csv_reader, range(data_matrix.shape[0])):
            results[i] = True
            csv_row = CsvRow(*row)
            for column_index, j in zip(
                data_extraction.COLUMNS_TO_EXTRACT,
                range(1, data_matrix.shape[1])
            ):
                csv_value = float(
                    csv_row[column_index] if csv_row[column_index] else 0.0
                )
                results[i] = results[i] and (csv_value == data_matrix[i, j])

        # Assert
        self.assertTrue(np.alltrue(results))

    def test_extracted_wiki_prices_data_tickers_ids(self):

        # Arrange
        csv_file = open(RAW_DATA_FILE_PATH)
        csv_reader = csv.reader(csv_file)
        data_matrix = np.load(EXTRACTED_DATA_FILE_PATH)
        companies_dict = pickle.load(open(COMPANIES_DICT_FILE_PATH, "rb"))
        CsvRow = namedtuple("CsvRow", data_extraction.CSV_ROW_FIELDS)
        results = np.empty([data_matrix.shape[0], ], dtype=np.bool)

        # Skip header row.
        next(csv_reader)

        # Act
        for row, i in zip(csv_reader, range(data_matrix.shape[0])):
            csv_row = CsvRow(*row)
            results[i] = companies_dict[csv_row.ticker] == \
                         int(data_matrix[i, 0])

        # Assert
        self.assertTrue(np.alltrue(results))


if __name__ == '__main__':
    unittest.main()