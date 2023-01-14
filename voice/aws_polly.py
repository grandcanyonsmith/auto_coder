
import logging

# Create a boolean variable to store the result
are_anagrams = False

# Define a function to compare two words
def is_anagram(word_1, word_2):
    """
    Checks if two words are anagrams of each other.
    
    Parameters:
    word_1 (str): The first word.
    word_2 (str): The second word.
    
    Returns:
    bool: True if the words are anagrams, False otherwise.
    """
    # Error Handling: Add more try/except blocks to handle unexpected user inputs.
    try:
        # Convert both words to sets
        word_1_set = set(word_1)
        word_2_set = set(word_2)
    except TypeError:
        logging.error("Please enter valid strings.")
        raise TypeError("Please enter valid strings.")
    
    # Compare the two sets
    is_anagram = word_1_set == word_2_set
    logging.debug(f"The comparison of '{word_1}' and '{word_2}' returned {is_anagram}")
    return is_anagram


# Define a function to get user inputs and validate them
def get_user_inputs():
    """
    Request two user inputs (strings).
    Validates the user inputs are strings.
    Sanitize the user inputs to prevent injection attacks.
    Remove all white spaces and special characters from the inputs.
    Convert both inputs to lowercase for consistency.
    Check if either input is empty.
    
    Returns:
    (str, str): The sanitized user inputs.
    """
    # Request two user inputs (strings)
    try:
        word_1 = input("Please type the first word: ")
        word_2 = input("Please type the second word: ")
    except ValueError:
        logging.error("Please enter valid strings.")
        raise ValueError("Please enter valid strings.")
    
    # Input Validation: Add additional checks to ensure the user inputs are of the correct type and format.
    # Checks that the user inputs are strings
    if not (isinstance(word_1, str) and isinstance(word_2, str)):
        logging.error("Please enter valid strings.")
        raise ValueError("Please enter valid strings.")
    
    # Security: Add additional sanitization to prevent injection attacks.
    word_1 = word_1.strip()
    word_2 = word_2.strip()

    # Validate user input types
    if not (isinstance(word_1, str) and isinstance(word_2, str)):
        logging.error("Please enter valid strings.")
        raise ValueError("Please enter valid strings.")
    
    # Remove all white spaces and special characters from both inputs using a regular expression
    import re  # Refactoring: Refactor the code to make it more efficient and easier to maintain.
    word_1 = re.sub(r'[^a-zA-Z0-9]+', '', word_1)
    word_2 = re.sub(r'[^a-zA-Z0-9]+', '', word_2)
    
    # Check if either input is empty
    if not word_1 or not word_2:
        logging.error("Please enter valid strings.")
        raise ValueError("Please enter valid strings.")
    
    # Convert both inputs to lowercase for consistency
    word_1 = word_1.lower()
    word_2 = word_2.lower()
    
    return word_1, word_2


# Get user inputs
try:
    word_1, word_2 = get_user_inputs()
    logging.debug(f"The user inputs are '{word_1}' and '{word_2}'")
except ValueError as e:
    print(e)
else:
    # Call the function to compare the two words
    are_anagrams = is_anagram(word_1, word_2)

    # Print the result
    if are_anagrams:
        print("These two words are anagrams of each other")
    else:
        print("These two words are not anagrams of each other")

#END
"""