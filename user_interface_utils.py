import inquirer
import logging
import unittest

# from auto_improve_ai import get_improvement_types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_suggestions_to_list(suggestions):
    """Converts a string of suggestions into a list."""
    try:
        # Strip the first line of the string and the last empty line
        return [suggestion.strip() for suggestion in suggestions.split("\n")[1:]][:-1]
    except Exception as e:
        logger.error(f"Error converting suggestions to list: {e}")


def strip_after_int(suggestion):
    """Strips everything after the int in the suggestion."""
    try:
        # Split the string on spaces and join the list back together, excluding the first element
        # add a 0 number with ALL to the beginning of the list

        # add 0. ALL to the beginning of the list        thne join the list back together
        return " ".join(suggestion.split(" ")[1:])

    except Exception as e:
        logger.error(f"Error stripping after int: {e}")


def add_number_to_selected_suggestions(selected_suggestions):
    """Adds int . to the beginning of each selected suggestion."""
    try:
        # Get the list of selected suggestions from the dictionary
        selected_suggestions = selected_suggestions["Changes to make"]
        # Iterate through the list and add the number to the beginning of each suggestion
        return [
            f"{i + 1}. {selected_suggestions[i]}"
            for i in range(len(selected_suggestions))
        ]
    except Exception as e:
        logger.error(f"Error adding number to selected suggestions: {e}")


def convert_list_to_string(selected_suggestions):
    """Converts a list of selected suggestions into a string    ."""
    try:
        # Join the list of selected suggestions into a string
        return "\n".join(selected_suggestions)
    except Exception as e:
        logger.error(f"Error converting list to string: {e}")


def let_user_select_which_changes(ai_generated_suggestions):
    """Allows the user to select which changes they would like to implement."""
    try:
        # Strip the int from the beginning of each suggestion
        ai_generated_suggestions = [
            strip_after_int(suggestion) for suggestion in ai_generated_suggestions
        ]
        # add 0. ALL to the beginning of the listF
        ai_generated_suggestions.insert(0, "All")
        ai_generated_suggestions.insert(1, "None")
        ai_generated_suggestions.insert(
            2, input("Enter your own suggestion: "))
        if "All" in ai_generated_suggestions:
            print("All")
        # Create a list of questions for the user to answer
        user_selected_suggestions = [
            inquirer.Checkbox(
                "Changes to make",
                message="Select which changes you would like to implement?",
                choices=ai_generated_suggestions,
            ),
            # inquirer.Confirm("confirm", message="Are you sure you want to make these changes?")
        ]
        # if "None", start over
        # if "None" in user_selected_suggestions:
        # get_improvement_types(file_contents)

        # get_improvement_suggestions(file_contents)
        # Get the user's selected suggestions and add the number to the beginning of each suggestion
        return add_number_to_selected_suggestions(
            inquirer.prompt(user_selected_suggestions)
        )
    except Exception as e:
        logger.error(f"Error letting user select which changes: {e}")


def allow_user_to_select_suggestions(ai_generated_suggestions):
    """Allows the user to select which suggestions they would like to implement."""
    try:
        # Convert the string of suggestions into a list
        ai_generated_suggestions = convert_suggestions_to_list(
            ai_generated_suggestions)
        # Let the user select which changes they would like to make
        selected_suggestions = let_user_select_which_changes(
            ai_generated_suggestions)
        # Convert the list of selected suggestions into a string
        selected_suggestions = convert_list_to_string(selected_suggestions)
        return selected_suggestions
    except Exception as e:
        logger.error(f"Error allowing user to select suggestions: {e}")


# Unit tests
class TestSuggestionFunctions(unittest.TestCase):
    def test_convert_suggestions_to_list(self):
        suggestions = (
            "1. Make changes to the code\n2. Add more features\n3. Optimize the code\n"
        )
        expected_result = [
            "Make changes to the code",
            "Add more features",
            "Optimize the code",
        ]
        self.assertEqual(convert_suggestions_to_list(
            suggestions), expected_result)

    def test_strip_after_int(self):
        suggestion = "1. Make changes to the code"
        expected_result = "Make changes to the code"
        self.assertEqual(strip_after_int(suggestion), expected_result)

    def test_add_number_to_selected_suggestions(self):
        selected_suggestions = {
            "Changes to make": [
                "Make changes to the code",
                "Add more features",
                "Optimize the code",
            ]
        }
        expected_result = [
            "1. Make changes to the code",
            "2. Add more features",
            "3. Optimize the code",
        ]
        self.assertEqual(
            add_number_to_selected_suggestions(
                selected_suggestions), expected_result
        )

    def test_convert_list_to_string(self):
        selected_suggestions = [
            "1. Make changes to the code",
            "2. Add more features",
            "3. Optimize the code",
        ]
        expected_result = (
            "1. Make changes to the code\n2. Add more features\n3. Optimize the code"
        )
        self.assertEqual(convert_list_to_string(
            selected_suggestions), expected_result)


if __name__ == "__main__":
    unittest.main()
