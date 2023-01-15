import csv
import json
import logging
import pathlib
from collections import namedtuple

logger = logging.getLogger(__name__)


class DuplicateFileNameError(Exception):
    """ Raised when a duplicate file name is found in the CSV. """
    pass


class FileDataManager:
    """
    Class to manage file data read from a csv file.
    """

    FileData = namedtuple('FileData', ['file_name', 'file_extension', 'description'])

    def __init__(self) -> None:
        self.data = {}

    def read_csv(self, csv_file: str, delimiter: str = ',') -> dict:
        """ Reads a csv into a dictionary and returns
        it. """
        data = {}
        with open(csv_file, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=delimiter)
            for row in reader:
                # skip the header row
                if row.get(reader.fieldnames[0], None) == reader.fieldnames[0]:
                    continue
                file_name = row.get(reader.fieldnames[0], None)
                description = row.get(reader.fieldnames[1], None)

                # Validate the data
                if not isinstance(file_name, str) or not isinstance(description, str) or len(file_name) > 255 or len(description) > 255:
                    logger.warning(f'Skipping row with malformed data {row}')
                    continue

                file_name, file_extension = pathlib.Path(file_name).stem, pathlib.Path(file_name).suffix

                # Check for duplicates
                if file_name in data:
                    logger.warning(f'Duplicate file name {file_name} found.')
                    raise DuplicateFileNameError(f'Duplicate file name {file_name} found.')

                file_data = self.FileData(file_name, file_extension, description)
                data[file_name] = file_data
        self.data = data
        return data

    def get_data(self) -> dict:
        """ Returns the data. """
        return self.data

    def check_duplicate_file_name(self, file_name):
        """ Checks for duplicate file name before writing the data to a CSV file. """
        if file_name in self.data:
            logger.warning(f'Duplicate file name {file_name} found.')
            raise DuplicateFileNameError(f'Duplicate file name {file_name} found.')
        return True

    def check_invalid_file_extension(self, file_extension):
        """ Checks for invalid file extensions before writing the data to a CSV file. """
        if file_extension not in ['.csv', '.html', '.json']:
            logger.warning(f'Invalid file extension {file_extension}.')
            raise ValueError(f'Invalid file extension {file_extension}.')
        return True

    def read_json(self, json_file: str) -> None:
        """ Reads the data from a JSON file. """
        with open(json_file, 'r') as json_file:
            data = json.load(json_file)
            for row in data:
                file_name = row.get('file_name', None)
                file_extension = pathlib.Path(file_name).suffix
                description = row.get('description', None)
                # Validate the data
                if not isinstance(file_name, str) or not isinstance(description, str) or len(file_name) > 255 or len(description) > 255:
                    logger.warning(f'Skipping row with malformed data {row}')
                    continue
                # Check for duplicates
                if self.check_duplicate_file_name(file_name):
                    logger.info(f'Checked for duplicate file name {file_name}.')
                # Check for invalid file extensions
                if self.check_invalid_file_extension(file_extension):
                    logger.info(f'Checked for invalid file extension {file_extension}.')
                file_name, file_extension = pathlib.Path(file_name).stem, pathlib.Path(file_name).suffix
                file_data = self.FileData(file_name, file_extension, description)
                self.data[file_name] = file_data

    def write_csv(self, csv_file: str) -> None:
        """ Writes the data to a csv file. """
        with open(csv_file, 'w') as csv_file:
            field_names = ['file_name', 'description']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for file_name, file_data in self.data.items():
                if self.check_duplicate_file_name(file_name):
                    logger.info(f'Checked for duplicate file name {file_name}.')
                if self.check_invalid_file_extension(file_data.file_extension):
                    logger.info(f'Checked for invalid file extension {file_data.file_extension}.')
                writer.writerow({
                    'file_name': f'{file_data.file_name}{file_data.file_extension}',
                    'description': file_data.description
                })

    def write_html(self, html_file: str) -> None:
        """ Writes the data to an HTML table. """
        with open(html_file, 'w') as html_file:
            html_file.write('<table>\n')
            html_file.write('  <tr>\n')
            html_file.write('    <th>File Name</th>\n')
            html_file.write('    <th>Description</th>\n')
            html_file.write('  </tr>\n')
            for file_name, file_data in self.data.items():
                if self.check_duplicate_file_name(file_name):
                    logger.info(f'Checked for duplicate file name {file_name}.')
                if self.check_invalid_file_extension(file_data.file_extension):
                    logger.info(f'Checked for invalid file extension {file_data.file_extension}.')
                html_file.write('  <tr>\n')
                html_file.write(f'    <td>{file_data.file_name}{file_data.file_extension}</td>\n')
                html_file.write(f'    <td>{file_data.description}</td>\n')
                html_file.write('  </tr>\n')
            html_file.write('</table>\n')

    def write_json(self, json_file: str) -> None:
        """ Writes the data to a JSON file. """
        with open(json_file, 'w') as json_file:
            data = [
                {
                    'file_name': f'{file_data.file_name}{file_data.file_extension}',
                    'description': file_data.description,
                }
                for file_name, file_data in self.data.items()
            ]
            json.dump(data, json_file)

    def write_sql(self, sql_file: str) -> None:
        """ Writes the data to a SQL database. """
        with open(sql_file, 'w') as sql_file:
            sql_file.write('CREATE TABLE IF NOT EXISTS file_data (\n')
            sql_file.write('  file_name VARCHAR(255) NOT NULL,\n')
            sql_file.write('  file_extension VARCHAR(255) NOT NULL,\n')
            sql_file.write('  description VARCHAR(255) NOT NULL\n')
            sql_file.write(');\n\n')
            for file_name, file_data in self.data.items():
                if self.check_duplicate_file_name(file_name):
                    logger.info(f'Checked for duplicate file name {file_name}.')
                if self.check_invalid_file_extension(file_data.file_extension):
                    logger.info(f'Checked for invalid file extension {file_data.file_extension}.')
                sql_file.write(f"INSERT INTO file_data VALUES ('{file_data.file_name}', '{file_data.file_extension}', '{file_data.description}');\n")

def main() -> None:
    """ Main function to run the program. """
    try:
        manager = FileDataManager()
        data = manager.read_csv('names_and_descriptions.csv')
        logger.info(f'Data read from csv file: {data}')
        manager.write_csv('output.csv')
        manager.write_html('output.html')
        manager.write_json('output.json')
        manager.write_sql('output.sql')
    except Exception as e:
        logger.exception(e)

if __name__ == '__main__':
    main()