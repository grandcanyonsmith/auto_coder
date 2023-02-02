class StringFormatter:
    def __init__(self):
        pass

    def remove_digits_and_period_from_string(self, string: str) -> str:
        """
        Removes any leading digit or period from the given string and returns the modified string.
        This function supports single digit, double digit, and multiple digit numbers, as well as numbers with decimal points.
        """
        while string[0].isdigit() or string[0] == "." or string[0] == " ":
            string = string[1:]
        return string

    def format_everything(self, list_of_strings: list) -> list:
        """
        Formats each string in the given list by removing any leading digit or period and capitalizing the first letter.
        This function supports single digit, double digit, and multiple digit numbers, as well as numbers with decimal points.
        """
        for i in range(len(list_of_strings)):
            list_of_strings[i] = self.remove_digits_and_period_from_string(list_of_strings[i])
            list_of_strings[i] = list_of_strings[i].capitalize()
        return list_of_strings