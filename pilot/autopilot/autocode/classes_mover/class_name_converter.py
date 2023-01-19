import re
import logging

class SnakeCaseConverter():
    '''
    Converts a given string to snake_case.
    '''

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def convert_string_to_snake_case(self, input_string):
        '''
        Convert the input string to snake_case.

        Args:
            input_string (str): The string to convert to snake_case.

        Returns:
            str: The converted string.
        '''
        output_string = "".join(
            f"_{char.lower()}" if (char.isupper()) else char
            for char in input_string
        )
        # Return the output string
        return f"{output_string}.py"

    def get_string_to_convert(self, input_string):
        '''
        Get the string from the user to convert.

        Returns:
            str: The string to convert.
        '''
        # input_string = ""
        while(not re.match("^[A-Za-z]+$", input_string)):
            try:
                input_string = input_string
            except Exception as e:
                self.logger.exception("Error while getting the string to convert")
            if(input_string == ""):
                print("Invalid input. Please enter a string: ")
        
        # Return the input string
        return input_string

class PythonFileCreator():
    '''
    Creates a python file with the given name.
    '''

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_python_file(self, file_name):
        '''
        Create a python file with the given name.

        Args:
            file_name (str): The name of the file to create.
        '''
        try:
            with open(file_name, "w") as f:
                f.write("import logging")
        except Exception as e:
            self.logger.exception("Error while creating the python file")

# if __name__ == "__main__":
#     # Create the logger
#     logging.basicConfig(
#         filename="log.txt",
#         filemode="w",
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#         level=logging.DEBUG
#     )
#     # Create the snake case converter
#     snake_case_converter = SnakeCaseConverter()
#     # Get the string to convert
#     list_of_classes = ["HelloWorld"] 
#     input_string = snake_case_converter.get_string_to_convert(list_of_classes[0])
#     # Convert the string to snake_case
#     output_string = snake_case_converter.convert_string_to_snake_case(input_string)
#     # Create the python file
#     python_file_creator = PythonFileCreator()
#     python_file_creator.create_python_file(output_string)