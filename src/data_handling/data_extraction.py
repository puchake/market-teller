import csv
import numpy as np
import pickle


# Input and output files paths.
RAW_DATA_FILE_PATH = "../../data/raw/wiki_prices_data.csv"
EXTRACTED_DATA_FILE_PATH = "../../data/extracted/wiki_prices_data.npy"
COMPANIES_DICT_FILE_PATH = "../../data/extracted/companies_dict.pickle"

# Ticker's name column index.
TICKER_COLUMN = 0

# Indices of elements from single data row which will be extracted.
COLUMNS_TO_EXTRACT = [2, 3, 4, 5, 6]


def read_raw_data_file(raw_data_file_path, columns_to_extract):
    """
    Read raw csv data file and return its rows as list of tuples. Also
    return dictionary of companies names.

    :param raw_data_file_path: path to file with unedited data
    :param columns_to_extract: indices of numeric csv columns which will be
                               extracted along with the first ticker column
    :return: list of tuples containing data
    """

    csv_file = open(raw_data_file_path, "r")
    csv_reader = csv.reader(csv_file)

    # Skip csv header, because it contains illegal characters and we can't
    # create named tuple directly from it.
    next(csv_reader)

    data_rows = []
    data_row_data = []
    companies_dict = dict()
    companies_counter = 0

    # Process each row from csv file.
    for row in csv_reader:
        csv_row = tuple(row)

        # If current row's ticker name is not present in companies dictionary,
        # save it in this dictionary along with current companies counter,
        # which will become this company id.
        if not csv_row[TICKER_COLUMN] in companies_dict:
            companies_dict[csv_row[TICKER_COLUMN]] = companies_counter
            companies_counter += 1

        # Append translated ticker name to data row's data as float to enable
        # straight conversion to numpy array.
        data_row_data.append(companies_dict[csv_row[TICKER_COLUMN]])

        for column_index in columns_to_extract:
            if csv_row[column_index]:

                # If this column's element in current row is not empty, append
                # its value converted to float to data row's data.
                data_row_data.append(float(csv_row[column_index]))

            else:
                data_row_data.append(0.0)
        data_rows.append(tuple(data_row_data))
        data_row_data.clear()

    return data_rows, companies_dict


if __name__ == "__main__":

    # Extract data.
    data_rows, companies_dict = read_raw_data_file(
        RAW_DATA_FILE_PATH, COLUMNS_TO_EXTRACT
    )
    data_matrix = np.array(data_rows)

    # Save data matrix and companies dictionary.
    np.save(EXTRACTED_DATA_FILE_PATH, data_matrix)
    pickle.dump(companies_dict, open(COMPANIES_DICT_FILE_PATH, "wb"))
