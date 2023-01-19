# This is a script to count the number of python classes in a list of files
import argparse
import ast
import os
import logging
import unittest
from class_name_converter import SnakeCaseConverter, PythonFileCreator

def parse_args() -> argparse.Namespace:
    """Set up argument parser and return parsed arguments."""
    parser = argparse.ArgumentParser(description="Count number of Python classes")
    parser.add_argument("--files", help="Path to files", nargs="+", required=True)
    parser.add_argument("--file_extensions", help="File extensions to search for", nargs="+", default=["py"])
    parser.add_argument("--output_formats", help="Output format", nargs="+", default=["txt"])
    parser.add_argument("-v", "--verbose", help="Verbose logging level", action="store_true")
    parser.add_argument("-d", "--debug", help="Debug logging level", action="store_true")
    parser.add_argument("-q", "--quiet", help="Quiet logging level", action="store_true")
    args = parser.parse_args()
    return args


def setup_logging(verbose: bool, debug: bool, quiet: bool) -> logging.Logger:
    """Set up logging."""
    if verbose:
        logging_level = logging.VERBOSE
    elif debug:
        logging_level = logging.DEBUG
    elif quiet:
        logging_level = logging.ERROR
    else:
        logging_level = logging.INFO
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger(__name__)
    return logger


def parse_and_validate_args(args: argparse.Namespace) -> list:
    """Parse and validate the given arguments."""
    # Validate file extensions
    if any(ext not in ["py", "txt", "csv"] for ext in args.file_extensions):
        raise ValueError("Invalid file extension")
    # Validate output formats
    if any(fmt not in ["txt", "csv"] for fmt in args.output_formats):
        raise ValueError("Invalid output format")
    # Get list of files with desired file extensions
    files = [file for file in args.files if any(file.endswith(ext) for ext in args.file_extensions)]
    # Validate files
    for f in files:
        if not os.path.exists(f):
            raise FileNotFoundError(f"File {f} does not exist")
    return files


def check_syntax(files: list) -> bool:
    """Check syntax before counting."""
    try:
        for f in files:
            ast.parse(open(f).read())
    except SyntaxError as err:
        logger.error(err)
        return False
    return True


def count_classes(files: list) -> int:
    """Count number of classes."""
    class_count = 0
    for f in files:
        with open(f) as file:
            for line in file:
                # Ignore commented lines
                if not line.startswith('#'):
                    if line.startswith('class'):
                        # Count classes that are capitolized
                        if line[6].isupper():
                            class_count += 1
    return class_count


def print_classes(files: list) -> None:
    """Print names of each class."""
    classes = []
    for f in files:
        with open(f) as file:
            for line in file:
                if not line.startswith('#'):
                    if line.startswith('class'):
                        # Save names of classes that are capitolized
                        if line[6].isupper():
                            classes.append(line[6:].split('(')[0].strip())
    print(f"Classes found: {classes}")
    return classes


def count_methods(files: list) -> None:
    """Count number of methods each class has."""
    methods = {}
    for f in files:
        with open(f) as file:
            for line in file:
                if (
                    not line.startswith('#')
                    and line.startswith('class')
                    and line[6].isupper()
                ):
                    class_name = line[6:].split('(')[0].strip()
                    method_lines = file.readlines()
                    method_count = sum(1 for l in method_lines if l.startswith('    def'))
                    methods[class_name] = method_count
    print(f"Methods found: {methods}")


def main() -> None:
    """Main function to run the script."""
    # Parse arguments
    args = parse_args()

    # Set up logging
    logger = setup_logging(args.verbose, args.debug, args.quiet)
    logger.info("Parsing arguments and validating files")

    # Parse and validate arguments
    files = parse_and_validate_args(args)

    # Check for valid syntax
    if check_syntax(files):
        # Count classes
        class_count = count_classes(files)
        print(f"Number of classes: {class_count}")

        # Print names of classes
        classes = print_classes(files)

        # Count number of methods
        count_methods(files)
    
        # Create the snake case converter
    snake_case_converter = SnakeCaseConverter()
    # Get the string to convert
    
    input_string = snake_case_converter.get_string_to_convert(classes[0])
    # Convert the string to snake_case
    output_string = snake_case_converter.convert_string_to_snake_case(input_string)
    # Create the python file
    python_file_creator = PythonFileCreator()
    python_file_creator.create_python_file(output_string)

# Unit tests
class TestCountClasses(unittest.TestCase):
    def test_count_classes(self):
        files = ["example.py"]
        class_count = count_classes(files)
        self.assertEqual(class_count, 2)

    def test_valid_file_extension(self):
        args = argparse.Namespace(files=["example.py"], file_extensions=["py"])
        files = parse_and_validate_args(args)
        self.assertEqual(files, ["example.py"])
    
    def test_invalid_file_extension(self):
        args = argparse.Namespace(files=["example.js"], file_extensions=["py"])
        with self.assertRaises(ValueError):
            files = parse_and_validate_args(args)
            self.assertEqual(files, [])
    
    def test_file_does_not_exist(self):
        args = argparse.Namespace(files=["not_a_file.py"], file_extensions=["py"])
        with self.assertRaises(FileNotFoundError):
            files = parse_and_validate_args(args)
            self.assertEqual(files, [])
    
    def test_valid_output_format(self):
        args = argparse.Namespace(files=["example.py"], file_extensions=["py"], output_formats=["txt"])
        files = parse_and_validate_args(args)
        self.assertEqual(files, ["example.py"])
    
    def test_invalid_output_format(self):
        args = argparse.Namespace(files=["example.py"], file_extensions=["py"], output_formats=["js"])
        with self.assertRaises(ValueError):
            files = parse_and_validate_args(args)
            self.assertEqual(files, [])

if __name__ == "__main__":
    # Run main function
    main()

