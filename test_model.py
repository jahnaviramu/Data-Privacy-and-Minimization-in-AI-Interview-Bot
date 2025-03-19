import json
from train import score_answer  # Importing a scoring function from the `train` module


def load_questions():
    """
    Loads the questions from the `questions.json` file.

    Returns:
        dict: A dictionary where keys are skills and values are lists of questions.

    Raises:
        FileNotFoundError: If the `questions.json` file does not exist.
        json.JSONDecodeError: If the file content is not a valid JSON.
    """
    try:
        # Open the questions.json file and load its content
        with open('questions.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Handle case where the file does not exist
        print("Error: 'questions.json' file not found.")
        return {}
    except json.JSONDecodeError as e:
        # Handle invalid JSON content in the file
        print(f"Error: Failed to decode 'questions.json' - {e}")
        return {}


def get_questions_by_skill(skill):
    """
    Fetches questions for a specific skill from the question bank.

    Args:
        skill (str): The skill for which questions are to be retrieved.

    Returns:
        list: A list of questions for the given skill. Returns an empty list if no questions are found.
    """
    try:
        # Load the questions dictionary
        questions = load_questions()
        # Return questions corresponding to the skill (case-insensitive)
        return questions.get(skill.lower(), [])
    except Exception as e:
        # Handle any unexpected errors during the process
        print(f"Error fetching questions for skill '{skill}': {e}")
        return []


def test_question(question_data, user_answer):
    """
    Evaluates the user's answer for a given question.

    Args:
        question_data (dict): A dictionary containing question details including the expected answer.
                              Example: {'question': 'What is Python?', 'expected_answer': 'A programming language'}
        user_answer (str): The answer provided by the user.

    Returns:
        tuple: A tuple containing the expected answer and the calculated score.

    Raises:
        KeyError: If the expected answer is not present in the `question_data`.
    """
    try:
        # Retrieve the expected answer from the question data
        expected_answer = question_data['expected_answer']
        # Use the `score_answer` function to calculate the score
        score = score_answer(expected_answer, user_answer)
        return expected_answer, score
    except KeyError:
        # Handle missing 'expected_answer' in question data
        print("Error: 'expected_answer' not found in the question data.")
        return None, 0
    except Exception as e:
        # Handle any unexpected errors during the evaluation
        print(f"Error testing question: {e}")
        return None, 0


# Example Usage
if __name__ == "__main__":
    # Example skill and user input for testing
    skill = "python"
    user_answer = "Python is a programming language."

    # Fetch questions for the skill
    skill_questions = get_questions_by_skill(skill)

    if skill_questions:
        print(f"Questions for '{skill}':")
        # Iterate through the list of questions for the skill
        for i, question_data in enumerate(skill_questions, start=1):
            print(f"Q{i}: {question_data['question']}")
            # Test the user's answer for the current question
            expected, score = test_question(question_data, user_answer)
            print(f"Your Answer: {user_answer}")
            print(f"Expected Answer: {expected}")
            print(f"Score: {score}")
    else:
        # Inform the user if no questions are found for the skill
        print(f"No questions found for skill '{skill}'.")
