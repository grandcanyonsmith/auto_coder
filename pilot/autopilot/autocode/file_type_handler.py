import logging

# Dictionary of file types
FILE_TYPES = {
    "py": "python script",
    "js": "javascript script",
    "rb": "ruby script",
    "php": "php script",
    "feature": "Gherkins feature",
    "txt": "Poem about being late",
}

class FileTypeHandler:
    """
    This class is used to detect the type of code file
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_file_type(self, file_path: str) -> str:
        """
        Gets the file type of the code file

        Args:
            file_path (str): The path to the file

        Returns:
            str: The file type
        """
        try:
            # Get the file extension
            file_extension = file_path.split(".")[-1]
            # Get the file type from the dictionary
            file_type = FILE_TYPES.get(file_extension, "unknown")
        except Exception:
            # Log the error
            self.logger.exception("Error getting file type")
            # Return unknown as the file type
            file_type = "unknown"
        return file_type