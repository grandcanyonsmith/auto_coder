import ast
import click
import logging
import os.path
from typing import Set, List, Any

# Set logging level
logging.basicConfig(level=logging.INFO)

def validate_inputs(filenames: List[str], class_name: str) -> bool:
    """Validate the filenames and class name arguments to ensure that they are valid.

    Parameters
    ----------
    filenames : List[str]
        The list containing the filename(s) to be checked. Must be valid strings and end with ".py".
    class_name : str
        The name of the class to be checked. Must be a valid string.

    Returns
    -------
    bool
        True if the inputs are valid, False otherwise.
    """
    # Check if the files exist
    for filename in filenames:
        if not os.path.exists(filename):
            logging.error(f'The given file {filename} does not exist.')
            return False

    # Check data types
    if not all(isinstance(filename, str) for filename in filenames):
        logging.error('The given filenames are not valid strings.')
        return False
    if not isinstance(class_name, str):
        logging.error('The given class name is not a valid string.')
        return False
    if not all(filename.endswith('.py') for filename in filenames):
        logging.error('The given files are not valid python files.')
        return False

    return True


def open_file(filename: str) -> str:
    """Open the given file in read mode and returns its contents.

    Parameters
    ----------
    filename : str
        The file to be opened. Must be a valid string.

    Returns
    -------
    str
        The contents of the file.
    """
    # Open the file in read mode
    try:
        with open(filename, 'r') as file_object:
            file_content = file_object.read()
    except OSError as e:
        logging.error(f'Error while opening file {filename}: {e}')
        raise e

    return file_content


def check_methods(file_content: str, class_name: str) -> Set[Any]:
    """Parse the file content using the ast module and checks for defined methods in the class.

    Parameters
    ----------
    file_content : str
        The contents of the file.
    class_name : str
        The name of the class to be checked. Must be a valid string.
    
    Returns
    -------
    set
        A set of all the methods in the class that are not defined in the file.
    """
    ast_tree = ast.parse(file_content)
    class_names = [node.name for node in ast.walk(ast_tree) if isinstance(node, ast.ClassDef)]
    if class_name not in class_names:
        logging.error(f'The given class name "{class_name}" is not defined in the file.')
        raise ValueError(f'The given class name "{class_name}" is not defined in the file.')
    else:
        logging.info(f'Checking methods of class "{class_name}"')
        undefined_methods = set()
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef) and node.name not in class_names:
                undefined_methods.add(node.name)

    return undefined_methods


def check_class_methods(filenames: List[str], class_name: str) -> Set[Any]:
    """Check a given file for a given class name and returns all the methods in the class that are not defined in the file.

    Parameters
    ----------
    filenames : List[str]
        The list containing the filename(s) to be checked. Must be valid strings and end with ".py".
    class_name : str
        The name of the class to be checked. Must be a valid string.

    Returns
    -------
    set
        A set of all the methods in the class that are not defined in the file.
    """
    # Create an empty set to store all the undefined methods
    undefined_methods: Set[Any] = set()

    # Validate inputs
    if not validate_inputs(filenames, class_name):
        raise ValueError('Invalid inputs!')
    logging.info('Checking files for class methods.')
    
    # Loop through all the filenames and check for any undefined methods
    for filename in filenames:
        # Open the file
        try:
            file_content = open_file(filename)
        except Exception as e:
            logging.error(e)
            raise e
        else:
            # Check for any undefined methods
            try:
                undefined_methods.update(check_methods(file_content, class_name))
            except Exception as e:
                logging.error(e)
                raise e
            else:
                logging.info('Checking file for class methods successful.')

    # Validate the output of the script
    if not isinstance(undefined_methods, Set):
        logging.error('Invalid output data type.')
        raise TypeError('Invalid output data type.')
    return undefined_methods


@click.command()
@click.option('--filenames', '-f', type=str, nargs='+', required=True,
                        help='List of python files to be checked. Must be valid strings and end with ".py".')
@click.option('--class_name', '-c', type=str, required=True,
                        help='Name of the class to be checked. Must be a valid string.')
@click.option('--log_level', '-l', type=click.Choice(['INFO', 'WARNING', 'ERROR', 'DEBUG']), default='INFO',
                        help='Logging level of the script.')
@click.option('--log_file', '-o', type=str, default=None,
                        help='Name of the file to write the logging messages.')
def main(filenames: List[str], class_name: str, log_level: str, log_file: str):
    """Check the class methods"""

    # Check that filenames is a list
    if not isinstance(filenames, list):
        raise TypeError('Filenames must be a list of strings.')
    
    # Set the logging level
    logging.basicConfig(level=logging.getLevelName(log_level))
    
    # Check for log file
    if log_file is not None:
        logging.basicConfig(filename=log_file)
    
    # Check the class methods
    try:
        undefined_methods = check_class_methods(filenames, class_name)
    except Exception as e:
        logging.error(e)
        raise e
    else:
        logging.info(f'Undefined methods: {undefined_methods}')
    

if __name__ == '__main__':
    main()
