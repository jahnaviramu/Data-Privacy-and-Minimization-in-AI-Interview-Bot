import os
from base64 import b64encode, b64decode

def encode_data(data):
    """
    Encode a string using Base64.

    Args:
        data (str): The string to encode.

    Returns:
        str: The Base64 encoded string.
    """
    try:
        # Convert the string to bytes, encode it to Base64, and return the encoded string
        return b64encode(data.encode()).decode()
    except Exception as e:
        # Handle any errors during the encoding process
        print(f"Error encoding data: {e}")
        return None


def decode_data(encoded_data):
    """
    Decode a Base64 encoded string.

    Args:
        encoded_data (str): The Base64 encoded string.

    Returns:
        str: The decoded string.
    """
    try:
        # Convert the Base64 encoded string to bytes, decode it, and return the decoded string
        return b64decode(encoded_data.encode()).decode()
    except Exception as e:
        # Handle any errors during the decoding process
        print(f"Error decoding data: {e}")
        return None


def encode_file(file_path):
    """
    Encode the content of a file using Base64 and save it with a .enc extension.

    Args:
        file_path (str): Path to the file to encode.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        # Read the file in binary mode
        with open(file_path, 'rb') as file:
            data = file.read()

        # Encode the file content using Base64
        encoded_data = b64encode(data).decode()

        # Save the encoded content to a new file with a .enc extension
        encoded_file_path = f"{file_path}.enc"
        with open(encoded_file_path, 'w') as enc_file:
            enc_file.write(encoded_data)

        print(f"File encoded successfully: {encoded_file_path}")
    except Exception as e:
        # Handle any errors during the file encoding process
        print(f"Error encoding file: {e}")


def decode_file(encoded_file_path):
    """
    Decode a Base64 encoded file and save the original content with a .dec extension.

    Args:
        encoded_file_path (str): Path to the encoded file.
    """
    # Check if the encoded file exists
    if not os.path.exists(encoded_file_path):
        print(f"Encoded file not found: {encoded_file_path}")
        return

    try:
        # Read the encoded file
        with open(encoded_file_path, 'r') as enc_file:
            encoded_data = enc_file.read()

        # Decode the Base64 content back to its original binary form
        decoded_data = b64decode(encoded_data.encode())

        # Save the decoded content to a new file with a .dec extension
        original_file_path = encoded_file_path.replace('.enc', '.dec')
        with open(original_file_path, 'wb') as dec_file:
            dec_file.write(decoded_data)

        print(f"File decoded successfully: {original_file_path}")
    except Exception as e:
        # Handle any errors during the file decoding process
        print(f"Error decoding file: {e}")
