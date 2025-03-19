import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Ensure necessary NLTK resources are downloaded
try:
    nltk.download('punkt', quiet=True)  # Download tokenizer data
    nltk.download('stopwords', quiet=True)  # Download stopwords data
except Exception as e:
    print(f"Error downloading NLTK resources: {e}")  # Handle any errors during the download


def clean_answer(answer):
    """
    Cleans and tokenizes the input answer by removing stopwords and punctuation.

    Args:
        answer (str): The input string to clean.

    Returns:
        list: A list of cleaned and tokenized words.
    """
    try:
        # Load English stopwords
        stop_words = set(stopwords.words('english'))
        # Tokenize the input answer into words
        tokens = word_tokenize(answer.lower())
        # Remove stopwords and punctuation from the tokens
        tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
        return tokens
    except Exception as e:
        # Handle unexpected errors during the cleaning process
        print(f"Error cleaning answer: {e}")
        return []


def score_answer(expected_answer, user_answer):
    """
    Scores the user's answer by comparing it with the expected answer using word matching.

    Args:
        expected_answer (str): The correct/expected answer.
        user_answer (str): The user's provided answer.

    Returns:
        float: A score between 0 and 10, representing the match percentage.
    """
    try:
        # Clean and tokenize the expected and user answers
        expected_tokens = clean_answer(expected_answer)
        user_tokens = clean_answer(user_answer)

        # Check if either answer is empty after cleaning
        if not expected_tokens or not user_tokens:
            print("Warning: One or both answers are empty after cleaning.")
            return 0.0

        # Find the common tokens between the two answers
        common_tokens = set(expected_tokens).intersection(user_tokens)
        match_score = len(common_tokens)

        # Calculate the maximum possible score based on token lengths
        max_score = max(len(expected_tokens), len(user_tokens))
        if max_score == 0:
            return 0.0  # Avoid division by zero

        # Compute the score as a percentage and scale to a 1-10 range
        score = (match_score / max_score) * 10
        return round(score, 2)  # Round to 2 decimal places
    except Exception as e:
        # Handle unexpected errors during scoring
        print(f"Error scoring answer: {e}")
        return 0.0


# Example Usage
if __name__ == "__main__":
    # Example inputs for testing
    expected = "Python is a powerful programming language."
    user = "Python is a programming language used for many purposes."

    print("Expected Answer:", expected)
    print("User Answer:", user)

    # Calculate the score for the user's answer
    score = score_answer(expected, user)

    # Output the calculated score
    print("Score:", score)
